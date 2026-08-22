
class JointPolicyPromotionGate:
    def __init__(self,min_samples=50,min_reward_gain=.02,max_success_drop=.01,max_violation_rate=.0,max_latency_increase=.15):
        self.min_samples=min_samples
        self.min_reward_gain=min_reward_gain
        self.max_success_drop=max_success_drop
        self.max_violation_rate=max_violation_rate
        self.max_latency_increase=max_latency_increase

    def evaluate(self,champion,challenger):
        reasons=[]
        if challenger.sample_count<self.min_samples:reasons.append("insufficient_samples")
        if challenger.reward<champion.reward+self.min_reward_gain:reasons.append("reward_gain_too_small")
        if challenger.success_rate<champion.success_rate-self.max_success_drop:reasons.append("success_guardrail")
        if challenger.violation_rate>self.max_violation_rate:reasons.append("violation_guardrail")
        base=max(1e-9,champion.latency_ms)
        if challenger.latency_ms>base*(1+self.max_latency_increase):reasons.append("latency_guardrail")
        return {"promote":not reasons,"reasons":reasons}
