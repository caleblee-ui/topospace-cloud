
class MetaUtility:
    def __init__(self,w_quality=.42,w_success=.22,w_cost=.14,w_latency=.10,w_violation=2.0,w_instability=.12):
        self.w_quality=w_quality;self.w_success=w_success;self.w_cost=w_cost
        self.w_latency=w_latency;self.w_violation=w_violation;self.w_instability=w_instability

    def score(self,o):
        cost_eff=1/(1+max(0,o.cost))
        lat_eff=1/(1+max(0,o.latency)/1000)
        return (self.w_quality*o.quality+self.w_success*o.success+
                self.w_cost*cost_eff+self.w_latency*lat_eff-
                self.w_violation*o.violations-self.w_instability*o.instability)
