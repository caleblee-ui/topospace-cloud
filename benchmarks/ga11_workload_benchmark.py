
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from optimization_plane.models import ExecutionCandidate,OptimizationBudget
from optimization_plane.runtime import OptimizationPlane
from joint_optimizer.objective import JointUtility
from joint_optimizer.models import JointObjective

rng=random.Random(202611)
vanilla_tokens=[];optimized_tokens=[]
vanilla_tools=[];optimized_tools=[]
vanilla_latency=[];optimized_latency=[]
quality=[]

for run in range(1200):
    candidates=[]
    for i in range(30):
        rel=i<8
        candidates.append(ExecutionCandidate(
          id=f"c{i}",
          kind="tool" if i%4==0 else "memory",
          distance=rng.uniform(.03,.25) if rel else rng.uniform(.35,1),
          utility=rng.uniform(.8,.98) if rel else rng.uniform(.15,.7),
          confidence=rng.uniform(.8,.98) if rel else rng.uniform(.2,.75),
          token_cost=rng.randint(100,450),
          latency_ms=rng.uniform(1,18),
          success_rate=rng.uniform(.8,.98) if rel else rng.uniform(.25,.7)
        ))
    vanilla_tokens.append(sum(x.token_cost for x in candidates))
    vanilla_tools.append(sum(x.kind=="tool" for x in candidates))
    vanilla_latency.append(sum(x.latency_ms for x in candidates))

    out=OptimizationPlane().plan(candidates,OptimizationBudget(max_tokens=3800,max_tool_calls=4,max_latency_ms=120,epsilon=.42))
    optimized_tokens.append(out["tokens"])
    optimized_tools.append(sum(x.kind=="tool" for x in out["selected"]))
    optimized_latency.append(out["latency_ms"])
    quality.append(sum(x.utility for x in out["selected"])/max(1,len(out["selected"])))

def reduction(a,b):
    return 100*(1-statistics.mean(b)/statistics.mean(a))

result={
 "runs":1200,
 "candidate_token_reduction_pct":reduction(vanilla_tokens,optimized_tokens),
 "candidate_tool_reduction_pct":reduction(vanilla_tools,optimized_tools),
 "candidate_latency_reduction_pct":reduction(vanilla_latency,optimized_latency),
 "mean_selected_utility":statistics.mean(quality),
 "note":"Synthetic GA workload harness. These are candidate-space reductions, not measured production LLM billing savings."
}
print(json.dumps(result,indent=2))
assert result["candidate_token_reduction_pct"]>30
assert result["candidate_tool_reduction_pct"]>20
assert result["mean_selected_utility"]>.75
Path("results/ga11_workload_benchmark.json").write_text(json.dumps(result,indent=2))
