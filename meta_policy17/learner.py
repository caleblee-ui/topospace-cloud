
from routing_policy14.models import RoutingOutcome
from learned_graph16.models import PathOutcome

class MetaPolicyLearner:
    def __init__(self,controller):
        self.controller=controller

    def update(self,decision,routing_ctx,quality,cost,latency,success,violations=0,reward=1.0):
        # Geometry receives the shared reward signal.
        geometry_reward=float(reward) - 2.0*violations - .05*max(0,cost) - .00005*max(0,latency)
        self.controller.geometry.update(
            decision["policy_state"],decision["geometry_decision"],geometry_reward
        )

        bucket=decision["model_route"]["bucket"]
        self.controller.model_policy.feedback(
          RoutingOutcome(
            decision["meta"].model,float(quality),
            int(getattr(routing_ctx,"expected_input_tokens",0)),
            int(getattr(routing_ctx,"expected_output_tokens",0)),
            float(latency),float(cost),bool(success),bucket
          )
        )

        graph_bucket=decision["graph_route"]["bucket"]
        self.controller.graph_policy.feedback(
          PathOutcome(graph_bucket,decision["meta"].path,float(reward),bool(success),float(cost),float(latency))
        )
