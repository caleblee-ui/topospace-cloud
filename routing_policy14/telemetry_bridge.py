
from routing_policy14.models import RoutingOutcome
from routing_policy14.features import topology_bucket
class RoutingTelemetryBridge:
    def __init__(self,policy):self.policy=policy
    def observe(self,ctx,model,usage,quality,cost,metadata=None):
        o=RoutingOutcome(model,float(quality),int(usage.input_tokens),int(usage.output_tokens),
                         float(usage.latency_ms),float(cost),bool(usage.success),topology_bucket(ctx),metadata or {})
        self.policy.feedback(o);return o
