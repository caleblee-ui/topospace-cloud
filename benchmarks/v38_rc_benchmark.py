
from pathlib import Path
import sys,json,time,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from commercial.service import CommercialTopoSpaceService
from compat.contract import ContractCompatibility
from e2e.torus_memory_path import TorusMemoryE2E
from faults.injector import FaultInjector
from install.doctor import doctor
from rc.version import VERSION

svc=CommercialTopoSpaceService()
req={"objective":"oauth repair","context":[{"id":"auth","tokens":200,"utility":.9,"distance":.1,"score":.9,"drift":.05},{"id":"noise","tokens":500,"utility":.1,"distance":.9,"score":.1,"drift":.8}]}
times=[];errors=0
for i in range(5000):
    try:
        t=time.perf_counter();out=svc.optimize(req,"rc-tenant","rc-project");times.append((time.perf_counter()-t)*1000)
    except Exception:errors+=1

contract=ContractCompatibility().validate_response(out)
torus=TorusMemoryE2E().run()
install=doctor(Path(__file__).resolve().parents[1])
fi=FaultInjector(17);fault_errors=0
for i in range(1000):
    try:fi.maybe_fail(.03)
    except Exception:fault_errors+=1

result={
 "version":VERSION,"iterations":5000,"service_error_rate":errors/5000,
 "p50_ms":statistics.median(times),"p95_ms":sorted(times)[int(.95*len(times))-1],
 "p99_ms":sorted(times)[int(.99*len(times))-1],"contract_ok":contract["ok"],
 "torus_e2e_visible":torus["visible"],"install_ok":install["ok"],
 "fault_injection_observed_rate":fault_errors/1000,
 "note":"In-process RC soak/fault regression; excludes external network, DB and LLM latency."
}
print(json.dumps(result,indent=2))
assert result["service_error_rate"]==0 and result["contract_ok"] and result["install_ok"]
assert "auth-decision" in result["torus_e2e_visible"]
Path("results/v38_rc_benchmark.json").write_text(json.dumps(result,indent=2))
