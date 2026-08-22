
from pathlib import Path
import sys,json,time,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from production.engine import TopoSpaceEngine

context=[
 {"id":"task","tokens":900,"utility":1,"distance":0,"score":1,"drift":0},
 {"id":"auth","tokens":5200,"utility":.95,"distance":.1,"score":.94,"drift":.05},
 {"id":"oauth","tokens":4800,"utility":.9,"distance":.14,"score":.88,"drift":.08},
 {"id":"tests","tokens":4100,"utility":.82,"distance":.22,"score":.8,"drift":.05},
 {"id":"logs","tokens":7600,"utility":.45,"distance":.31,"score":.48,"drift":.2},
 {"id":"frontend","tokens":6800,"utility":.1,"distance":.72,"score":.14,"drift":.55},
 {"id":"old","tokens":9300,"utility":.08,"distance":.81,"score":.12,"drift":.7},
]
agents=[
 {"id":"coding","capabilities":["code"],"score":.94,"reliability":.96,"cost":.2,"risk":.08},
 {"id":"security","capabilities":["security"],"score":.9,"reliability":.97,"cost":.2,"risk":.05},
 {"id":"test","capabilities":["test"],"score":.86,"reliability":.96,"cost":.18,"risk":.05},
 {"id":"front","capabilities":["frontend"],"score":.1,"reliability":.9,"cost":.15,"risk":.1},
]
e=TopoSpaceEngine()
times=[]
for i in range(1000):
 t=time.perf_counter();r=e.optimize("Fix OAuth vulnerability",context,agents,["code","security","test"]);times.append((time.perf_counter()-t)*1000)
base=sum(x["tokens"] for x in context)
saving=100*(1-r["context_tokens"]/base)
out={"raw_context_tokens":base,"optimized_context_tokens":r["context_tokens"],"context_reduction_pct":saving,
     "team":[x["id"] for x in r["team"]],"p50_engine_ms":statistics.median(times),
     "p95_engine_ms":sorted(times)[949],"health":e.health(),
     "note":"Engine microbenchmark and deterministic context fixture; not an LLM marketing claim."}
print(json.dumps(out,indent=2))
assert saving>30 and [x["id"] for x in r["team"]]==["coding","security","test"]
Path("results/v19_engine_benchmark.json").write_text(json.dumps(out,indent=2))
