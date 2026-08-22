
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unified_runtime.models import AgentState
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder
from unified_runtime.runtime import UnifiedAdaptiveAgentRuntime
from coupled_geometry.runtime import CrossDomainGeometryRuntime

rng=random.Random(1729);builder=RuntimeSpaceBuilder()
domains=("memory","tool","skill","plan")
independent_selected=[];coupled_selected=[];coupled_iters=[];violations=0

for run in range(300):
    spaces={}
    for d in domains:
        rows=[]
        for i in range(32):
            good=i<7
            rows.append({
              "id":f"{d}-{run}-{i}","kind":d,
              "semantic_distance":rng.uniform(.03,.18) if good else rng.uniform(.28,.95),
              "structural_distance":rng.uniform(.03,.22) if good else rng.uniform(.25,.9),
              "history_distance":rng.uniform(.04,.25) if good else rng.uniform(.2,.85),
              "policy_distance":0 if good else (1 if d in {"tool","plan"} and rng.random()<.22 else 0),
              "security_distance":0 if good else (1 if d=="tool" and rng.random()<.18 else 0),
              "cost_distance":rng.uniform(.04,.35),
              "reliability_distance":rng.uniform(.03,.2) if good else rng.uniform(.2,.75),
            })
        spaces[d]=builder.build_space(rows)

    state=AgentState(f"t{run}","task",risk=rng.random(),ambiguity=rng.random(),
                     hierarchy=rng.random(),candidate_pressure=rng.random(),
                     latency_pressure=rng.random())

    independent=UnifiedAdaptiveAgentRuntime().build_execution_space(state,spaces)
    independent_selected.append(sum(len(independent["routes"][d]["selected"]) for d in domains))

    coupled=CrossDomainGeometryRuntime(max_iterations=4).solve(state,spaces)
    coupled_selected.append(sum(len(coupled["routes"][d]["selected"]) for d in domains))
    coupled_iters.append(coupled["joint_state"].iteration)

    for d in ("tool","plan"):
        for x in coupled["routes"][d]["selected"]:
            p=x["payload"]
            if p.get("policy_distance",0)>=1 or p.get("security_distance",0)>=1:
                violations+=1

out={
 "runs":300,
 "mean_independent_selected":statistics.mean(independent_selected),
 "mean_coupled_selected":statistics.mean(coupled_selected),
 "mean_joint_iterations":statistics.mean(coupled_iters),
 "selection_change_pct":100*(statistics.mean(coupled_selected)-statistics.mean(independent_selected))/statistics.mean(independent_selected),
 "policy_security_violations_selected":violations,
 "note":"Synthetic cross-domain coupling benchmark. Selection change measures coupled-vs-independent runtime behavior, not production quality improvement."
}
print(json.dumps(out,indent=2))
assert out["policy_security_violations_selected"]==0
assert out["mean_joint_iterations"]>=1
assert abs(out["selection_change_pct"])>.1
Path("results/beta7_coupled_geometry_benchmark.json").write_text(json.dumps(out,indent=2))
