from __future__ import annotations
import time,uuid
from production.adaptive_engine import AdaptiveTopoSpaceEngine
from commercial.schemas import validate_optimize_request
from commercial.errors import TopoSpaceError
from commercial.sla import SLATracker
class CommercialTopoSpaceService:
    VERSION="3.0.0-alpha"
    def __init__(self,engine=None): self.engine=engine or AdaptiveTopoSpaceEngine();self.sla=SLATracker()
    def optimize(self,request,tenant_id="default",project_id="default"):
        errors=validate_optimize_request(request)
        if errors: raise TopoSpaceError("INVALID_REQUEST",",".join(errors),False,400)
        req_id=request.get("request_id") or uuid.uuid4().hex; started=time.perf_counter()
        try:
            out=self.engine.optimize_adaptive(objective=request["objective"],context=request.get("context",[]),agents=request.get("agents",[]),required_capabilities=request.get("required_capabilities",[]),uncertainty=request.get("uncertainty",.3),drift=request.get("drift",0),previous_success=request.get("previous_success",True),cost_pressure=request.get("cost_pressure",.5),complexity=request.get("complexity",.5))
            elapsed=(time.perf_counter()-started)*1000;self.sla.record(elapsed,False)
            return {"api_version":"v1","engine_version":self.VERSION,"request_id":req_id,"tenant_id":tenant_id,"project_id":project_id,"result":out,"latency_ms":elapsed}
        except TopoSpaceError: raise
        except Exception as e:
            elapsed=(time.perf_counter()-started)*1000;self.sla.record(elapsed,True);raise TopoSpaceError("ENGINE_FAILURE",str(e),True,500)
