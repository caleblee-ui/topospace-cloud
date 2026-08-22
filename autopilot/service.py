
from __future__ import annotations
from customer.service import CustomerTopoSpaceService
from autopilot.runtime import AutopilotRuntime
from autopilot.models import RuntimeSignals

class AutopilotTopoSpaceService(CustomerTopoSpaceService):
    def __init__(self,engine=None,meter=None,autopilot=None):
        super().__init__(engine,meter)
        self.autopilot=autopilot or AutopilotRuntime()

    def optimize_with_autopilot(self,request,tenant_id="default",project_id="default",signals=None):
        signals=signals or RuntimeSignals(
            success_rate=float(request.get("success_rate",.9)),
            uncertainty=float(request.get("uncertainty",.3)),
            drift=float(request.get("drift",.1)),
            token_pressure=float(request.get("token_pressure",.5)),
            latency_pressure=float(request.get("latency_pressure",.3)),
            tool_failure_rate=float(request.get("tool_failure_rate",0)),
            memory_hit_rate=float(request.get("memory_hit_rate",.7)),
        )
        auto=self.autopilot.update(signals)
        d=auto["decision"]
        req=dict(request)
        req["uncertainty"]=signals.uncertainty
        req["drift"]=signals.drift
        req["complexity"]=max(float(req.get("complexity",.5)),d["exploration"])
        out=super().optimize(req,tenant_id,project_id)
        out["autopilot"]=auto
        out["result"]["adaptive"]["epsilon"]=d["epsilon"]
        out["result"]["adaptive"]["p"]=d["p"]
        out["result"]["adaptive"]["max_context_tokens"]=d["max_context_tokens"]
        out["result"]["adaptive"]["memory_recall_limit"]=d["memory_recall_limit"]
        out["result"]["adaptive"]["tool_radius"]=d["tool_radius"]
        return out
