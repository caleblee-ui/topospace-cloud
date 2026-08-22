
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class TopologyNode:
    id:str
    distance:float
    utility:float=0.5
    tokens:int=0
    level:int=0
    payload:dict|None=None

class HierarchicalTopology:
    """Partitions candidates into coarse epsilon shells before fine ranking."""
    def __init__(self, shells=(.15,.35,.65,1.0)):
        self.shells=tuple(shells)

    def level_for(self,distance):
        d=max(0.0,float(distance))
        for i,e in enumerate(self.shells):
            if d<=e:return i
        return len(self.shells)

    def organize(self,nodes):
        out={}
        for n in nodes:
            level=self.level_for(n.distance)
            n.level=level
            out.setdefault(level,[]).append(n)
        for level in out:
            out[level].sort(key=lambda n:(n.distance,-n.utility,n.tokens))
        return out
