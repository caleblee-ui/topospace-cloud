
from pathlib import Path
import sys,time,statistics,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_sdk.middleware import TopoSpaceMiddleware
from runtime_sdk.adapter import AgentRuntimeAdapter
m=TopoSpaceMiddleware();a=AgentRuntimeAdapter(m,"bench")
lat=[]
for i in range(5000):
 t=f"t{i}";s=time.perf_counter()
 a.task_start(t);a.before_model(t,prompt="x");a.after_model(t,answer="y")
 a.before_tool(t,"tool");a.after_tool(t,"tool",True,reward=.9);a.task_complete(t,True)
 lat.append((time.perf_counter()-s)*1000)
out={"runs":5000,"mean_full_lifecycle_ms":statistics.mean(lat),"p95_full_lifecycle_ms":sorted(lat)[int(.95*len(lat))-1],"hooks_per_run":6,"note":"In-process middleware overhead only; excludes LLM/tool/network/storage latency."}
print(json.dumps(out,indent=2));assert out["p95_full_lifecycle_ms"]<5
Path("results/alpha8_runtime_sdk_benchmark.json").write_text(json.dumps(out,indent=2))
