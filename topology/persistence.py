
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass
class PersistenceInterval:
    component: str
    birth: float
    death: float|None
    persistence: float|None

class UnionFind:
    def __init__(self):
        self.parent={}
    def add(self,x): self.parent.setdefault(x,x)
    def find(self,x):
        p=self.parent[x]
        if p!=x:self.parent[x]=self.find(p)
        return self.parent[x]
    def union(self,a,b):
        ra,rb=self.find(a),self.find(b)
        if ra==rb:return False
        self.parent[rb]=ra
        return True

def zero_dim_persistence(nodes: List[str], weighted_edges: List[Tuple[str,str,float]]):
    """Computes a simple 0-dimensional persistence barcode from edge thresholds.

    Each node is born at epsilon=0. Components merge as epsilon reaches edge weight.
    The younger/root component dies at the merge threshold. One component persists forever.
    """
    uf=UnionFind()
    birth={n:0.0 for n in nodes}
    label={n:n for n in nodes}
    for n in nodes: uf.add(n)
    intervals=[]
    for a,b,w in sorted(weighted_edges,key=lambda x:x[2]):
        if a not in uf.parent or b not in uf.parent: continue
        ra,rb=uf.find(a),uf.find(b)
        if ra==rb: continue
        la,lb=label[ra],label[rb]
        # deterministic elder rule by label
        if la <= lb:
            keep,die=ra,rb; keep_label,die_label=la,lb
        else:
            keep,die=rb,ra; keep_label,die_label=lb,la
        uf.parent[die]=keep
        label[keep]=keep_label
        intervals.append(PersistenceInterval(die_label,birth[die_label],float(w),float(w)-birth[die_label]))
    roots={uf.find(n) for n in nodes}
    survivors=sorted({label[r] for r in roots})
    for s in survivors:
        intervals.append(PersistenceInterval(s,birth[s],None,None))
    return intervals
