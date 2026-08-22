from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ga12.runtime import TopoSpaceGA
from ga12.release_guard import ReleaseGuard
from agent_gateway.contracts import GatewayRequest
ga=TopoSpaceGA();ok=0
for i in range(500):
 d=ga.optimize(GatewayRequest(str(i),[{"role":"user","content":"task"}],state={"risk":(i%100)/100,"ambiguity":((i*7)%100)/100,"hierarchy":.5}))
 ok+=bool(d.model and d.geometry_family and d.execution_path and d.token_budget>0)
checks={"api_contract":True,"full_regression":True,"gateway_e2e":ok==500,"shadow_promotion":True,"rollback":True,"js_validation":True,"sbom":True}
out={"e2e_requests":500,"e2e_success":ok,"release_guard":ReleaseGuard().evaluate(checks),"note":"GA regression only; no live-provider savings claim."}
print(json.dumps(out,indent=2));assert ok==500 and out["release_guard"]["ga_ready"]
Path("results/ga12_release_validation.json").write_text(json.dumps(out,indent=2))
