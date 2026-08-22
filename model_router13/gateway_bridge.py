
from model_router13.context_builder import RoutingContextBuilder

class TopologyAwareGatewayRouter:
    def __init__(self,router):
        self.router=router
        self.builder=RoutingContextBuilder()

    def apply(self,req,gateway_decision):
        ctx=self.builder.from_gateway(req,gateway_decision)
        routed=self.router.route(ctx)
        gateway_decision.model=routed["selected"]
        gateway_decision.diagnostics["model_ranking"]=routed["ranking"]
        gateway_decision.diagnostics["routing_context"]=ctx.__dict__
        return gateway_decision
