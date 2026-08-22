
from __future__ import annotations
from production.engine import TopoSpaceEngine
from production.config import ProductionConfig
from optimization.adaptive_controller import AdaptiveOptimizationController
from optimization.quality_guard import QualityPreservationGuard
from optimization.token_optimizer import TokenBudgetController, TokenBudget

class AdaptiveTopoSpaceEngine(TopoSpaceEngine):
    """Production engine with per-request adaptive topology parameters."""
    def __init__(self,config=None,controller=None,quality_guard=None):
        super().__init__(config or ProductionConfig())
        self.controller=controller or AdaptiveOptimizationController()
        self.quality_guard=quality_guard or QualityPreservationGuard()

    def optimize_adaptive(self,objective,context,agents=None,required_capabilities=None,
                          uncertainty=.3,drift=.0,previous_success=True,cost_pressure=.5,complexity=.5):
        decision=self.controller.decide(
            uncertainty=uncertainty,drift=drift,previous_success=previous_success,
            cost_pressure=cost_pressure,complexity=complexity)
        old_token=self.token
        try:
            p=self.pruner.prune(context,decision["epsilon"],self.config.min_relevance,self.config.max_drift)
            dynamic_token=TokenBudgetController(TokenBudget(decision["max_context_tokens"],self.config.reserve_output_tokens))
            b=dynamic_token.prune(p["kept"])
            team=self.team.optimize(agents or [],required_capabilities or [],min_marginal_utility=.20,max_agents=self.config.max_agents)
            q=self.quality_guard.should_expand(uncertainty=uncertainty,previous_success=previous_success,kept_items=len(b["kept"]))
            # quality fallback: if over-pruned, expand once to the configured maximum epsilon/budget
            expanded=False
            if q["expand"]:
                expanded=True
                ep=self.controller.policy.epsilon_max
                p2=self.pruner.prune(context,ep,self.config.min_relevance,self.config.max_drift)
                max_token=TokenBudgetController(TokenBudget(self.controller.policy.token_budget_max,self.config.reserve_output_tokens))
                b=max_token.prune(p2["kept"])
            return {
              "objective":objective,"context":b["kept"],"dropped_context":[x for x in context if x not in b["kept"]],
              "context_tokens":b["tokens"],"team":team,"adaptive":decision,
              "quality_guard":q,"expanded_for_quality":expanded,
              "guardrails":self.guard.validate(agents=len(team))
            }
        except Exception:
            if not self.config.fail_open: raise
            return super().optimize(objective,context,agents,required_capabilities)
        finally:
            self.token=old_token
