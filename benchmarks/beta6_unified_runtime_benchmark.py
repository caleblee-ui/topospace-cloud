
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from unified_runtime.models import AgentState
from unified_runtime.runtime import UnifiedAdaptiveAgentRuntime
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder

rng=random.Random(1729);builder=RuntimeSpaceBuilder()
domains=("memory","tool","skill","plan")
selected={d:[] for d in domains};violations={d:0 for d in domains};blocked={d:[] for d in domains}
families={d:{} for d in domains}

for run in range(400):
    raw={}
    for d in domains:
        rows=[]
        for i in range(30):
            good=i<6
            rows.append({
              "id":f"{d}-{run}-{i}","kind":d,
              "semantic_distance":rng.uniform(.03,.2) if good else rng.uniform(.25,.95),
              "structural_distance":rng.uniform(.03,.25) if good else rng.uniform(.2,.9),
              "history_distance":rng.uniform(.05,.3) if good else rng.uniform(.2,.9),
              "policy_distance":0 if good else (1.0 if d in {"tool","plan"} and rng.random()<.25 else 0),
              "security_distance":0 if good else (1.0 if d=="tool" and rng.random()<.2 else 0),
              "cost_distance":rng.uniform(.05,.4),
              "reliability_distance":rng.uniform(.03,.25) if good else rng.uniform(.15,.75),
            })
        raw[d]=builder.build_space(rows)

    state=AgentState(f"t{run}","task",
      risk=rng.random(),ambiguity=rng.random(),hierarchy=rng.random(),
      candidate_pressure=rng.random(),latency_pressure=rng.random())
    result=UnifiedAdaptiveAgentRuntime().build_execution_space(state,raw)

    for d in domains:
        route=result["routes"][d]
        sel=route["selected"]
        selected[d].append(len(sel))
        blocked[d].append(len(route.get("blocked_by_constraints",[])))
        fam=result["geometry"][d]["aggregator"]
        families[d][fam]=families[d].get(fam,0)+1
        for x in sel:
            p=x["payload"]
            if p.get("policy_distance",0)>=1 or p.get("security_distance",0)>=1:
                violations[d]+=1

out={
 "runs":400,
 "mean_selected":{d:statistics.mean(selected[d]) for d in domains},
 "mean_blocked_by_hard_constraints":{d:statistics.mean(blocked[d]) for d in domains},
 "geometry_family_usage":families,
 "selected_policy_or_security_violations":violations,
 "note":"Synthetic unified-runtime routing benchmark. Demonstrates shared adaptive geometry plus hard constraint gating across four runtime domains, not production task quality."
}
print(json.dumps(out,indent=2))

assert sum(families["tool"].values())==400
assert len(families["memory"])>=2
assert violations["tool"]==0
assert violations["plan"]==0
assert statistics.mean(blocked["tool"])>0
Path("results/beta6_unified_runtime_benchmark.json").write_text(json.dumps(out,indent=2))
