
from __future__ import annotations
from commercial.service import CommercialTopoSpaceService
from customer.metering import UsageMeter

class CustomerTopoSpaceService(CommercialTopoSpaceService):
    def __init__(self,engine=None,meter=None):
        super().__init__(engine)
        self.meter=meter or UsageMeter()

    def optimize(self,request,tenant_id="default",project_id="default"):
        out=super().optimize(request,tenant_id,project_id)
        result=out["result"]
        self.meter.record(tenant_id,"optimization_requests",1,{"project_id":project_id})
        self.meter.record(tenant_id,"optimized_context_tokens",result.get("context_tokens",0),{"project_id":project_id})
        self.meter.record(tenant_id,"agent_count",len(result.get("team",[])),{"project_id":project_id})
        return out
