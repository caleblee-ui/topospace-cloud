
from pathlib import Path
import sys,json,time,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from commercial.service import CommercialTopoSpaceService
from e2e.torus_http_smoke import run_http_e2e
from install.doctor import doctor
from ga.version import VERSION

svc=CommercialTopoSpaceService()
req={"objective":"ga smoke","context":[{"id":"a","tokens":100,"utility":1,"distance":.1,"score":.9,"drift":.05}]}
times=[];errors=0
for i in range(10000):
    try:
        t=time.perf_counter();svc.optimize(req,"ga","ga");times.append((time.perf_counter()-t)*1000)
    except Exception:errors+=1

torus=run_http_e2e()
install=doctor(Path(__file__).resolve().parents[1])
out={
 "version":VERSION,
 "iterations":10000,
 "service_error_rate":errors/10000,
 "p50_ms":statistics.median(times),
 "p95_ms":sorted(times)[int(.95*len(times))-1],
 "p99_ms":sorted(times)[int(.99*len(times))-1],
 "torus_http_e2e":torus["ok"],
 "install_ok":install["ok"],
 "note":"GA in-process runtime soak plus local HTTP TorusDB-adapter smoke. External production services are not included."
}
print(json.dumps(out,indent=2))
assert out["service_error_rate"]==0 and out["torus_http_e2e"] and out["install_ok"]
Path("results/v100_ga_benchmark.json").write_text(json.dumps(out,indent=2))
