
class ConstrainedEfficiencyObjective:
    """Reward efficiency only when quality guardrails are satisfied."""
    def __init__(self,min_success_rate=.90,max_latency_norm=1.0):
        self.min_success_rate=min_success_rate
        self.max_latency_norm=max_latency_norm

    def evaluate(self,*,success_rate,token_reduction,cost_reduction,latency_norm,risk=0.0):
        feasible=(success_rate>=self.min_success_rate and latency_norm<=self.max_latency_norm and risk<=.75)
        reward=(.45*token_reduction+.35*cost_reduction+.20*(1-latency_norm)-.30*risk)
        if not feasible:
            reward-=1.0+(self.min_success_rate-success_rate if success_rate<self.min_success_rate else 0)
        return {"reward":reward,"feasible":feasible}
