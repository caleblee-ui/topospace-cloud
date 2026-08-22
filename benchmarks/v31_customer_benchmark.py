
from pathlib import Path
import sys,time,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from customer.service import CustomerTopoSpaceService

svc=CustomerTopoSpaceService()
req={"objective":"customer test","context":[
 {"id":"a","tokens":500,"utility":.9,"distance":.1,"score":.9,"drift":.05},
 {"id":"b","tokens":900,"utility":.1,"distance":.8,"score":.1,"drift":.7}
]}
times=[]
for i in range(1000):
    t=time.perf_counter();svc.optimize(req,"tenant-a","project-a");times.append((time.perf_counter()-t)*1000)
out={
 "iterations":len(times),
 "p50_ms":statistics.median(times),
 "p95_ms":sorted(times)[949],
 "metered_requests":svc.meter.total("tenant-a","optimization_requests"),
 "note":"In-process customer service benchmark; excludes network, OIDC, external stores."
}
print(json.dumps(out,indent=2))
assert out["metered_requests"]==1000
Path("results/v31_customer_benchmark.json").write_text(json.dumps(out,indent=2))
