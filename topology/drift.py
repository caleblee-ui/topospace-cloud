
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable, Dict, Set, Any
import math

@dataclass
class DriftReport:
    jaccard_drift: float
    density_drift: float
    component_drift: float
    score: float
    entered: list
    exited: list

def _components(nodes, edges):
    adj={n:set() for n in nodes}
    for a,b in edges:
        if a in adj and b in adj:
            adj[a].add(b); adj[b].add(a)
    seen=set(); c=0
    for n in nodes:
        if n in seen: continue
        c+=1; stack=[n]; seen.add(n)
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)
    return c

class TopologicalDrift:
    """Measures structural change between two neighborhood snapshots."""

    def compare(self, previous: Dict[str,Any], current: Dict[str,Any]) -> DriftReport:
        pn=set(previous.get("nodes",[])); cn=set(current.get("nodes",[]))
        inter=len(pn & cn); union=len(pn | cn)
        jaccard = 1.0 - (inter/union if union else 1.0)

        def density(snap):
            nodes=set(snap.get("nodes",[])); edges=snap.get("edges",[])
            n=len(nodes)
            if n < 2: return 0.0
            valid=sum(1 for a,b in edges if a in nodes and b in nodes and a!=b)
            return min(1.0, (2.0*valid)/(n*(n-1)))

        pd, cd = density(previous), density(current)
        density_drift = abs(cd-pd)

        pc=_components(pn, previous.get("edges",[]))
        cc=_components(cn, current.get("edges",[]))
        component_drift = abs(cc-pc)/max(1,pc,cc)

        score = 0.6*jaccard + 0.25*density_drift + 0.15*component_drift
        return DriftReport(
            jaccard, density_drift, component_drift, min(1.0,score),
            sorted(cn-pn), sorted(pn-cn)
        )
