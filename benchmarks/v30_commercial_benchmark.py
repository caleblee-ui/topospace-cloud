
from pathlib import Path
import sys,time,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from commercial.service import CommercialTopoSpaceService
svc=CommercialTopoSpaceService();req={"objective":"secure oauth","context":[{"id":"auth","tokens":800,"utility":.9,"distance":.1,"score":.9,"drift":.05},{"id":"test","tokens":700,"utility":.8,"distance":.2,"score":.8,"drift":.05},{"id":"noise","tokens":1400,"utility":.1,"distance":.8,"score":.1,"drift":.7}],"agents":[{"id":"coding","capabilities":["code"],"score":.9,"reliability":.95,"cost":.2,"risk":.05}],"required_capabilities":["code"],"uncertainty":.2,"complexity":.3,"cost_pressure":.8}
times=[]
for i in range(2000):
 t=time.perf_counter();out=svc.optimize(req,"bench","p");times.append((time.perf_counter()-t)*1000)
result={"iterations":len(times),"p50_service_ms":statistics.median(times),"p95_service_ms":sorted(times)[int(.95*len(times))-1],"p99_service_ms":sorted(times)[int(.99*len(times))-1],"sla":svc.sla.snapshot(),"note":"In-process service benchmark; excludes network/external storage."}
print(json.dumps(result,indent=2));assert out["result"]["context"]
Path("results/v30_commercial_benchmark.json").write_text(json.dumps(result,indent=2))
