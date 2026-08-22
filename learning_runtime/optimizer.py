
from __future__ import annotations
import random, math

class BayesianStyleOptimizer:
    """Dependency-free local surrogate search around observed good configurations.

    This is deliberately conservative: it mutates around the best feasible observations
    rather than claiming a full Gaussian-process implementation.
    """
    def __init__(self,seed=41):
        self.rng=random.Random(seed)
        self.history=[]

    def observe(self,params,reward,feasible=True):
        self.history.append({"params":dict(params),"reward":float(reward),"feasible":bool(feasible)})

    def suggest(self,bounds):
        feasible=[x for x in self.history if x["feasible"]]
        if not feasible:
            return {k:(lo+hi)/2 for k,(lo,hi) in bounds.items()}
        best=max(feasible,key=lambda x:x["reward"])["params"]
        out={}
        for k,(lo,hi) in bounds.items():
            center=float(best.get(k,(lo+hi)/2))
            sigma=(hi-lo)*.12
            out[k]=max(lo,min(hi,self.rng.gauss(center,sigma)))
        return out
