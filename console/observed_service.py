
from customer.service import CustomerTopoSpaceService
from console.operations import OperationsStore

class ObservedCustomerService(CustomerTopoSpaceService):
    def __init__(self,engine=None,meter=None,operations=None):
        super().__init__(engine,meter);self.operations=operations or OperationsStore()

    def optimize(self,request,tenant_id="default",project_id="default"):
        out=super().optimize(request,tenant_id,project_id)
        result=out["result"]
        self.operations.record(
          "optimization",tenant_id,
          request_id=out["request_id"],project_id=project_id,
          objective=request["objective"],latency_ms=out["latency_ms"],
          context_tokens=result.get("context_tokens",0),
          selected_context=result.get("context",[]),
          team=result.get("team",[]),
          adaptive=result.get("adaptive",{})
        )
        return out
