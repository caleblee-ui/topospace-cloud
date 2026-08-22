
from model_router13.context_builder import RoutingContextBuilder
from unified_runtime.models import AgentState

class MetaPolicyGatewayBridge:
    def __init__(self,meta_runtime):
        self.runtime=meta_runtime
        self.context_builder=RoutingContextBuilder()

    def apply(self,req,gateway_decision):
        routing_ctx=self.context_builder.from_gateway(req,gateway_decision)
        state=AgentState(
          req.task_id,req.metadata.get("objective","agent-task"),
          risk=float(req.state.get("risk",0)),
          ambiguity=float(req.state.get("ambiguity",0)),
          hierarchy=float(req.state.get("hierarchy",0)),
          candidate_pressure=float(req.state.get("candidate_pressure",0)),
          latency_pressure=float(req.state.get("latency_pressure",0)),
          metadata=dict(req.state.get("metadata",{}))
        )
        decision=self.runtime.decide(state,routing_ctx)
        live=decision["live"]["meta"]
        gateway_decision.model=live.model
        gateway_decision.diagnostics["meta_geometry"]=live.geometry_family
        gateway_decision.diagnostics["meta_path"]=live.path
        gateway_decision.diagnostics["meta_score"]=live.score
        gateway_decision.diagnostics["meta_overrides"]=decision["live"].get("meta_overrides",[])
        return gateway_decision
