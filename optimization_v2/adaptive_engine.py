
from optimization_v2.adaptive_metric import DynamicPNorm,AdaptiveEpsilon
from optimization_v2.engine import OptimizationEngineV2
from optimization_v2.context_compiler import TopologyContextCompiler
from optimization_v2.topology_cache import TopologyCache

class AdaptiveOptimizationEngine:
    def __init__(self):
        self.metric=DynamicPNorm();self.epsilon=AdaptiveEpsilon()
        self.base=OptimizationEngineV2();self.compiler=TopologyContextCompiler();self.cache=TopologyCache()

    def optimize(self,objective,items,token_budget=4000):
        vectors=[[float(x.get("score",0)),float(x.get("utility",x.get("importance",.5))),1-float(x.get("distance",1))] for x in items]
        p=self.metric.choose_p(vectors)
        eps=self.epsilon.choose([float(x.get("distance",1)) for x in items])
        key=self.cache.key(objective,items,p,eps)
        cached=self.cache.get(key)
        if cached is not None:
            out=dict(cached);out["cache_hit"]=True;return out
        enriched=[]
        for x in items:
            y=dict(x)
            # Adaptive epsilon normalizes local topological distance without changing public schema.
            y["distance"]=min(1.0,float(x.get("distance",1))/max(eps,1e-9)) if float(x.get("distance",1))<=eps else min(1.0,float(x.get("distance",1)))
            enriched.append(y)
        selected=self.base.optimize(enriched,token_budget)
        compiled=self.compiler.compile(objective,selected["context"],token_budget)
        out={**selected,"p":p,"epsilon":eps,"compiled":compiled,"cache_hit":False}
        self.cache.set(key,out)
        return out
