
from learned_graph16.models import PathOutcome
from learned_graph16.bucket import graph_topology_bucket

class ExecutionGraphTelemetryBridge:
    def __init__(self,policy):self.policy=policy

    def observe(self,ctx,path_name,reward,success,cost,latency_ms):
        o=PathOutcome(graph_topology_bucket(ctx),path_name,float(reward),bool(success),float(cost),float(latency_ms))
        self.policy.feedback(o)
        return o
