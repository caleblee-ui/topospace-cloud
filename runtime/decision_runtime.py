
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from runtime.hybrid_context import HybridTopologicalScorer, HybridWeights

@dataclass
class Candidate:
    id: str
    type: str
    adaptive_distance: float
    persistence: float = 0.0
    drift: float = 0.0
    metadata: Dict[str,Any] = field(default_factory=dict)

@dataclass
class Decision:
    selected: List[dict]
    rejected: List[dict]
    budget: int
    reason: str

class TopoDecisionRuntime:
    """Selects agent-visible objects from the current state neighborhood."""

    def __init__(self, scorer: HybridTopologicalScorer|None=None):
        self.scorer=scorer or HybridTopologicalScorer()

    def select(self, candidates: List[Candidate], weighted_edges, budget: int = 8, allowed_types=None):
        allowed=set(allowed_types) if allowed_types else None
        nodes=[c.id for c in candidates if allowed is None or c.type in allowed]
        byid={c.id:c for c in candidates if c.id in nodes}
        dist={c.id:c.adaptive_distance for c in byid.values()}
        pers={c.id:c.persistence for c in byid.values()}
        drift={c.id:c.drift for c in byid.values()}
        edges=[e for e in weighted_edges if e[0] in byid and e[1] in byid]

        ranked=self.scorer.score(nodes,edges,dist,pers,drift)
        selected=[]
        for row in ranked[:max(0,int(budget))]:
            c=byid[row["id"]]
            selected.append({
                "id":c.id,"type":c.type,"score":row["score"],
                "components":row["components"],
                "topological_support":row.get("topological_support",0.0),
                "metadata":c.metadata
            })
        chosen={x["id"] for x in selected}
        rejected=[{"id":c.id,"type":c.type} for c in byid.values() if c.id not in chosen]
        return Decision(selected,rejected,budget,"hybrid topological relevance")

    def select_by_type(self, candidates, weighted_edges, budgets: Dict[str,int]):
        out={}
        for typ,budget in budgets.items():
            out[typ]=self.select(candidates,weighted_edges,budget,[typ])
        return out
