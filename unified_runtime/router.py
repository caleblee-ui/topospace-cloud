
from geometry_policy.model import PolicyState
from geometry_policy.controller import AdaptiveGeometryController
from geometry_policy.network import GeometryPolicyNetwork
from geometry_policy.reward import geometry_reward
from unified_runtime.constraints import HardConstraintGate

class UnifiedAdaptiveRouter:
    DOMAINS=("memory","tool","skill","plan")

    def __init__(self,n_views=7):
        self.policy=GeometryPolicyNetwork(n_views=n_views)
        self.controller=AdaptiveGeometryController(self.policy)
        self.constraints=HardConstraintGate()

    def _state(self,agent_state,domain):
        return PolicyState(
            task_type=domain,
            risk=min(1.0,agent_state.risk + (.12 if domain in {"tool","plan"} else 0)),
            ambiguity=min(1.0,agent_state.ambiguity + (.10 if domain=="memory" else 0)),
            hierarchy=min(1.0,agent_state.hierarchy + (.12 if domain=="plan" else 0)),
            candidate_pressure=agent_state.candidate_pressure,
            latency_pressure=agent_state.latency_pressure,
        )

    def route(self,agent_state,domain,candidates):
        if domain not in self.DOMAINS:
            raise ValueError("unknown_domain")
        s=self._state(agent_state,domain)

        # Tool and planning spaces are operationally actionable; hard policy/security
        # constraints are therefore enforced before any compensatory geometry.
        hard_gate = domain in {"tool","plan"}
        gated,blocked=self.constraints.filter(candidates,enabled=hard_gate)

        result=self.controller.retrieve(s,gated)
        result["domain"]=domain
        result["policy_state"]=s
        result["blocked_by_constraints"]=[x["id"] for x in blocked]
        return result

    def feedback(self,route_result,relevant_selected,total_relevant,violations=0,latency_ms=0,token_cost=0):
        selected_count=len(route_result["selected"])
        reward=geometry_reward(relevant_selected,total_relevant,selected_count,violations,latency_ms,token_cost)
        self.controller.feedback(route_result["policy_state"],route_result["decision"],reward)
        return reward
