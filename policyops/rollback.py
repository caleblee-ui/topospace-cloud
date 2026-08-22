
class AutomaticRollback:
    def __init__(self,max_error_rate=.08,max_success_drop=.05,max_latency_increase=.35):
        self.max_error_rate=max_error_rate;self.max_success_drop=max_success_drop;self.max_latency_increase=max_latency_increase

    def check(self,baseline,current):
        reasons=[]
        if current.get("error_rate",0)>self.max_error_rate:reasons.append("error_rate")
        if current.get("success_rate",1)<baseline.get("success_rate",1)-self.max_success_drop:reasons.append("success_drop")
        b=max(1e-9,baseline.get("p95_ms",1))
        if (current.get("p95_ms",b)-b)/b>self.max_latency_increase:reasons.append("latency_regression")
        return {"rollback":bool(reasons),"reasons":reasons}
