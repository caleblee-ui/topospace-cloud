
from pathlib import Path
import sys,json,random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from autopilot.self_optimizing import SelfOptimizingAutopilot
from autopilot.models import RuntimeSignals

a=SelfOptimizingAutopilot();rng=random.Random(5)
rows=[]
for i in range(180):
    sig=RuntimeSignals(success_rate=.94,uncertainty=.22,drift=.10,token_pressure=.82,latency_pressure=.55,tool_failure_rate=.03,memory_hit_rate=.82)
    d=a.decide(sig)
    profile=d["decision"]["profile"]
    # deterministic synthetic environment: efficient is best while still feasible
    perf={
      "conservative":(.97,.22,.18,.72),
      "balanced":(.96,.38,.31,.64),
      "efficient":(.94,.52,.46,.59),
    }[profile]
    score=a.learn(d,success_rate=perf[0],token_reduction=perf[1],cost_reduction=perf[2],latency_norm=perf[3],risk=.05)
    rows.append({"profile":profile,"reward":score["reward"],"feasible":score["feasible"]})
tail=rows[-60:]
counts={p:sum(1 for x in tail if x["profile"]==p) for p in a.PROFILES}
out={"tail_profile_counts":counts,"observations":len(rows),"note":"Synthetic learning convergence fixture; not customer performance evidence."}
print(json.dumps(out,indent=2))
assert counts["efficient"]>counts["conservative"]
Path("results/v34_learning_benchmark.json").write_text(json.dumps(out,indent=2))
