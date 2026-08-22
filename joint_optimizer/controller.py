
from geometry_policy.model import PolicyState
from geometry_policy.network import GeometryPolicyNetwork
from learned_field.models import FieldState
from learned_field.network import CouplingFieldNetwork
from joint_optimizer.models import JointDecision

class JointGeometryController:
    """
    Coordinates local geometry A_theta and cross-domain coupling field C_theta(s).
    """
    def __init__(self):
        self.geometry=GeometryPolicyNetwork()
        self.field=CouplingFieldNetwork()

    def decide(self,agent_state):
        ps=PolicyState(
          risk=agent_state.risk,
          ambiguity=agent_state.ambiguity,
          hierarchy=agent_state.hierarchy,
          candidate_pressure=agent_state.candidate_pressure,
          latency_pressure=agent_state.latency_pressure
        )
        fs=FieldState(
          risk=agent_state.risk,
          ambiguity=agent_state.ambiguity,
          hierarchy=agent_state.hierarchy,
          candidate_pressure=agent_state.candidate_pressure,
          latency_pressure=agent_state.latency_pressure,
          memory_pressure=float(agent_state.metadata.get("memory_pressure",0)),
          tool_pressure=float(agent_state.metadata.get("tool_pressure",0)),
        )
        gd=self.geometry.decide(ps)
        field=self.field.forward(fs)
        aggregate=.6*gd.confidence+.4*field.confidence
        return {
          "policy_state":ps,
          "field_state":fs,
          "geometry":gd,
          "field":field,
          "joint":JointDecision(gd.aggregator,gd.epsilon,gd.p,field.confidence,aggregate)
        }

    def update(self,decision,rewards_by_domain,joint_reward):
        # Shared reward updates both local geometry and field.
        self.geometry.update(decision["policy_state"],decision["geometry"],joint_reward)
        self.field.update(decision["field_state"],rewards_by_domain)
