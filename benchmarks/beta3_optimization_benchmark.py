
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from optimization_plane.models import ExecutionCandidate,OptimizationBudget
from optimization_plane.runtime import OptimizationPlane
rng=random.Random(1729)
base_tokens=[];opt_tokens=[];base_tools=[];opt_tools=[];base_latency=[];opt_latency=[];quality=[]
for run in range(1000):
 candidates=[]
 for i in range(24):
  relevant=i<7
  candidates.append(ExecutionCandidate(
   f"c{i}","tool" if i%3==0 else "memory",
   rng.uniform(.03,.32) if relevant else rng.uniform(.45,1),
   rng.uniform(.75,.98) if relevant else rng.uniform(.15,.7),
   rng.uniform(.75,.98) if relevant else rng.uniform(.3,.75),
   rng.randint(120,500),rng.uniform(1,15),
   rng.uniform(.75,.98) if relevant else rng.uniform(.25,.7)))
 base_tokens.append(sum(x.token_cost for x in candidates))
 base_tools.append(sum(x.kind=="tool" for x in candidates))
 base_latency.append(sum(x.latency_ms for x in candidates))
 budget=OptimizationBudget(max_tokens=3500,max_tool_calls=4,max_latency_ms=100,epsilon=.38)
 o=OptimizationPlane().plan(candidates,budget)
 opt_tokens.append(o["tokens"]);opt_tools.append(sum(x.kind=="tool" for x in o["selected"]));opt_latency.append(o["latency_ms"])
 quality.append(sum(x.utility for x in o["selected"])/max(1,len(o["selected"])))
def saving(a,b):return 100*(1-statistics.mean(b)/statistics.mean(a))
out={"runs":1000,"token_reduction_pct":saving(base_tokens,opt_tokens),"tool_call_reduction_pct":saving(base_tools,opt_tools),"candidate_latency_reduction_pct":saving(base_latency,opt_latency),"mean_selected_utility":statistics.mean(quality),"note":"Synthetic candidate-selection workload. Reductions are engine benchmark results, not claims about production LLM bills or end-user task quality."}
print(json.dumps(out,indent=2))
assert out["token_reduction_pct"]>30 and out["tool_call_reduction_pct"]>20 and out["mean_selected_utility"]>.7
Path("results/beta3_optimization_benchmark.json").write_text(json.dumps(out,indent=2))
