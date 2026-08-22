
from __future__ import annotations
from dataclasses import dataclass
from itertools import combinations
from typing import Iterable, List, Tuple, Dict, Set

@dataclass(frozen=True)
class Simplex:
    vertices: tuple
    filtration: float

class VietorisRipsComplex:
    """Builds a Vietoris-Rips complex up to dimension 2 from weighted pair distances."""
    def build(self, nodes: List[str], weighted_edges: List[Tuple[str,str,float]], epsilon: float):
        dist={}
        simplices=[]
        for n in nodes:
            simplices.append(Simplex((n,),0.0))
        for a,b,w in weighted_edges:
            dist[frozenset((a,b))]=float(w)
            if w <= epsilon:
                simplices.append(Simplex(tuple(sorted((a,b))),float(w)))
        # triangles appear when all three edges are present
        for a,b,c in combinations(nodes,3):
            ws=[]
            ok=True
            for x,y in ((a,b),(a,c),(b,c)):
                key=frozenset((x,y))
                if key not in dist or dist[key] > epsilon:
                    ok=False; break
                ws.append(dist[key])
            if ok:
                simplices.append(Simplex(tuple(sorted((a,b,c))),max(ws)))
        return simplices
