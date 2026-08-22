
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from execution_graph15.planner import TopologyAwareExecutionGraphPlanner
from model_router13.models import RoutingContext

rng=random.Random(1205);planner=TopologyAwareExecutionGraphPlanner()
single_model_cost=[];graph_expected_cost=[];escalation_nodes=[]

cost={"fast":1.0,"balanced":3.0,"reasoning":9.0}
for _ in range(5000):
    ctx=RoutingContext(risk=rng.random(),ambiguity=rng.random(),topology_complexity=rng.random(),
                       coupling_strength=rng.random(),expected_tool_calls=rng.randint(0,6))
    complexity=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity,ctx.coupling_strength)
    # Baseline sends any non-trivial task directly to reasoning.
    baseline="reasoning" if complexity>.35 else "balanced"
    single_model_cost.append(cost[baseline])

    primary="fast" if complexity<.3 else ("balanced" if complexity<.75 else "reasoning")
    g=planner.build(ctx,{"selected":primary},ctx.expected_tool_calls>0,True)

    # Expected graph cost: escalation nodes weighted by probability of needing escalation.
    c=0.0
    for n in g.nodes:
        if n.kind!="model":continue
        if n.metadata.get("role")=="primary":
            c+=cost[n.model]
        else:
            prob=.15 if complexity<.5 else (.35 if complexity<.75 else .55)
            c+=prob*cost[n.model]
    graph_expected_cost.append(c)
    escalation_nodes.append(sum(n.metadata.get("role")=="escalation" for n in g.nodes if n.kind=="model"))

out={
 "runs":5000,
 "baseline_mean_model_cost_units":statistics.mean(single_model_cost),
 "graph_expected_model_cost_units":statistics.mean(graph_expected_cost),
 "expected_model_cost_reduction_pct":100*(1-statistics.mean(graph_expected_cost)/statistics.mean(single_model_cost)),
 "mean_escalation_nodes":statistics.mean(escalation_nodes),
 "note":"Synthetic expected-cost benchmark. Cost units and escalation probabilities are constructed for regression, not live provider billing."
}
print(json.dumps(out,indent=2))
assert out["expected_model_cost_reduction_pct"]>10
Path("results/beta12_execution_graph_benchmark.json").write_text(json.dumps(out,indent=2))
