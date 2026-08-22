
class JointAutomaticRollback:
    def __init__(self,max_error_rate=.05,max_violation_rate=.0,max_reward_drop=.05,max_latency_increase=.20):
        self.max_error_rate=max_error_rate
        self.max_violation_rate=max_violation_rate
        self.max_reward_drop=max_reward_drop
        self.max_latency_increase=max_latency_increase

    def check(self,baseline,current):
        reasons=[]
        if current.get("error_rate",0)>self.max_error_rate:reasons.append("error_rate")
        if current.get("violation_rate",0)>self.max_violation_rate:reasons.append("violation_rate")
        if current.get("reward",0)<baseline.get("reward",0)-self.max_reward_drop:reasons.append("reward_drop")
        b=max(1e-9,baseline.get("latency_ms",1))
        if current.get("latency_ms",b)>b*(1+self.max_latency_increase):reasons.append("latency_regression")
        return {"rollback":bool(reasons),"reasons":reasons}
