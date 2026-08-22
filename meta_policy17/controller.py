
from geometry_policy.network import GeometryPolicyNetwork
from geometry_policy.model import PolicyState
from model_router13.default_profiles import default_profiles
from routing_policy14.policy import LearnedModelRoutingPolicy
from learned_graph16.templates import default_path_templates
from learned_graph16.policy import LearnedExecutionGraphPolicy
from model_router13.models import RoutingContext
from meta_policy17.models import MetaDecision

class MetaPolicyController:
    """
    Coordinates three learned layers:
      1) generalized geometry
      2) model routing
      3) execution graph path
    """
    def __init__(self):
        self.geometry=GeometryPolicyNetwork()
        self.model_policy=LearnedModelRoutingPolicy(default_profiles())
        self.graph_policy=LearnedExecutionGraphPolicy(default_path_templates())

    def decide(self,agent_state,routing_ctx):
        ps=PolicyState(
          risk=agent_state.risk,ambiguity=agent_state.ambiguity,hierarchy=agent_state.hierarchy,
          candidate_pressure=agent_state.candidate_pressure,latency_pressure=agent_state.latency_pressure
        )
        gd=self.geometry.decide(ps)
        mr=self.model_policy.route(routing_ctx)
        gp=self.graph_policy.route(routing_ctx)

        # Meta confidence is intentionally transparent, not a learned black box yet.
        score=.34*gd.confidence+.33*mr["ranking"][0]["utility"]+.33*gp["ranking"][0]["utility"]
        return {
          "policy_state":ps,
          "geometry_decision":gd,
          "model_route":mr,
          "graph_route":gp,
          "meta":MetaDecision(gd.aggregator,gd.epsilon,gd.p,mr["selected"],gp["selected"],score)
        }
