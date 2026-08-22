
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass
class AdaptivePolicy:
    epsilon_min: float=.18
    epsilon_max: float=.65
    token_budget_min: int=8000
    token_budget_max: int=48000
    p_min: float=1.0
    p_max: float=4.0
    uncertainty_expand: float=.65
    failure_expand: float=.18
    cost_pressure: float=.20

class AdaptiveOptimizationController:
    """Dynamically controls epsilon, Lp exponent and context budget.

    Low uncertainty/cost-sensitive tasks contract the neighborhood.
    High uncertainty, failure or structural drift expands it.
    """
    def __init__(self,policy=None):
        self.policy=policy or AdaptivePolicy()

    @staticmethod
    def _clip(x,a,b): return max(a,min(b,x))

    def decide(self,*,uncertainty=.3,drift=.0,previous_success=True,cost_pressure=.5,complexity=.5):
        p=self.policy
        uncertainty=self._clip(float(uncertainty),0,1)
        drift=self._clip(float(drift),0,1)
        complexity=self._clip(float(complexity),0,1)
        cost_pressure=self._clip(float(cost_pressure),0,1)

        need=.45*uncertainty+.25*drift+.30*complexity
        if not previous_success: need=self._clip(need+p.failure_expand,0,1)

        epsilon=p.epsilon_min+(p.epsilon_max-p.epsilon_min)*need
        epsilon-=p.cost_pressure*cost_pressure*(1-uncertainty)
        epsilon=self._clip(epsilon,p.epsilon_min,p.epsilon_max)

        budget_need=self._clip(.55*need+.45*uncertainty-.20*cost_pressure,0,1)
        tokens=round(p.token_budget_min+(p.token_budget_max-p.token_budget_min)*budget_need)

        # Higher p emphasizes dominant coordinate deviations; lower p broadens aggregate similarity.
        lp=p.p_min+(p.p_max-p.p_min)*self._clip(.55*complexity+.45*uncertainty,0,1)

        return {"epsilon":epsilon,"max_context_tokens":tokens,"p":lp,
                "need":need,"uncertainty":uncertainty,"drift":drift,
                "cost_pressure":cost_pressure,"complexity":complexity}
