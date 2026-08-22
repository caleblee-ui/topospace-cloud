
from collections import defaultdict
from routing_policy14.models import RoutingWeights
class RoutingPolicyLearner:
    def __init__(self,weights=None,prior_strength=4):
        self.weights=weights or RoutingWeights();self.prior_strength=prior_strength
        self.stats=defaultdict(lambda:{"n":0,"quality":0.0,"cost":0.0,"latency":0.0,"success":0.0})
    def observe(self,o):
        s=self.stats[(o.topology_bucket,o.model)];s["n"]+=1;s["quality"]+=o.quality;s["cost"]+=o.cost
        s["latency"]+=o.latency_ms;s["success"]+=1 if o.success else 0
    def empirical(self,b,m,p):
        s=self.stats[(b,m)];n=s["n"];k=self.prior_strength
        return {"n":n,"quality":(s["quality"]+k*p.quality)/(n+k),
                "success":(s["success"]+k*.8)/(n+k),
                "latency":(s["latency"]+k*p.latency_ms)/(n+k),
                "cost":(s["cost"]+k*(p.input_cost_per_1k+p.output_cost_per_1k))/(n+k)}
    def utility(self,b,p):
        e=self.empirical(b,p.name,p);w=self.weights
        cost_eff=1/(1+e["cost"]);lat_eff=1/(1+e["latency"]/1000)
        return w.quality*e["quality"]+w.cost*cost_eff+w.latency*lat_eff+w.success*e["success"]
