
from dataclasses import dataclass
from typing import List

@dataclass
class ProviderEndpoint:
    id:str
    model:str
    latency_ms:float
    cost_per_1k:float
    reliability:float
    max_context:int
    healthy:bool=True

class ProviderRouter:
    """Selects provider/model under latency, cost, reliability and context constraints."""
    def select(self,endpoints:List[ProviderEndpoint],required_context:int,
               latency_weight=.35,cost_weight=.35,reliability_weight=.30):
        candidates=[e for e in endpoints if e.healthy and e.max_context>=required_context]
        if not candidates:return None
        max_lat=max(e.latency_ms for e in candidates) or 1
        max_cost=max(e.cost_per_1k for e in candidates) or 1
        def score(e):
            lat=1-e.latency_ms/max_lat
            cost=1-e.cost_per_1k/max_cost
            rel=e.reliability
            return latency_weight*lat+cost_weight*cost+reliability_weight*rel
        return max(candidates,key=score)
