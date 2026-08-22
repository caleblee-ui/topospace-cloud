
from __future__ import annotations
from dataclasses import dataclass
from heapq import heappush, heappop
from typing import Dict, List, Tuple

@dataclass
class PlanResult:
    path:list
    cost:float
    visited:int

class TopologicalPlanner:
    """Shortest-path planner with topology-aware penalties."""
    def __init__(self, risk_weight=.6, drift_weight=.5, persistence_bonus=.35):
        self.risk_weight=risk_weight
        self.drift_weight=drift_weight
        self.persistence_bonus=persistence_bonus

    def plan(self, start, goal, adjacency, node_meta=None):
        node_meta=node_meta or {}
        pq=[(0.0,start,[start])]; best={start:0.0}; visited=0
        while pq:
            cost,u,path=heappop(pq);visited+=1
            if u==goal:return PlanResult(path,cost,visited)
            if cost!=best.get(u):continue
            for v,base in adjacency.get(u,[]):
                m=node_meta.get(v,{})
                step=float(base)
                step += self.risk_weight*float(m.get("risk",0))
                step += self.drift_weight*float(m.get("drift",0))
                step -= self.persistence_bonus*float(m.get("persistence",0))
                step=max(0.001,step)
                nc=cost+step
                if nc < best.get(v,float("inf")):
                    best[v]=nc;heappush(pq,(nc,v,path+[v]))
        return PlanResult([],float("inf"),visited)
