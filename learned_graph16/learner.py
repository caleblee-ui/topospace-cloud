
from collections import defaultdict

class ExecutionGraphPolicyLearner:
    def __init__(self,prior_strength=5):
        self.prior_strength=prior_strength
        self.stats=defaultdict(lambda:{"n":0,"reward":0.0,"success":0,"cost":0.0,"latency":0.0})

    def observe(self,outcome):
        s=self.stats[(outcome.topology_bucket,outcome.path_name)]
        s["n"]+=1;s["reward"]+=outcome.reward;s["success"]+=1 if outcome.success else 0
        s["cost"]+=outcome.cost;s["latency"]+=outcome.latency_ms

    def utility(self,bucket,path):
        s=self.stats[(bucket,path.name)];n=s["n"];k=self.prior_strength
        # Priors favor cheap paths until data shows escalation is worth it.
        prior_reward=max(.45,min(.85,.78-.02*path.nominal_cost))
        reward=(s["reward"]+k*prior_reward)/(n+k)
        success=(s["success"]+k*.75)/(n+k)
        cost=(s["cost"]+k*path.nominal_cost)/(n+k)
        latency=(s["latency"]+k*path.nominal_latency_ms)/(n+k)
        cost_eff=1/(1+cost/4)
        lat_eff=1/(1+latency/1000)
        return .52*reward+.22*success+.14*cost_eff+.12*lat_eff
