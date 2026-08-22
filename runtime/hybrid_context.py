
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict
from typing import Dict

@dataclass
class HybridWeights:
    adaptive: float = 0.42
    structural: float = 0.24
    persistence: float = 0.22
    drift_stability: float = 0.12

class HybridTopologicalScorer:
    """Hybrid context scorer with topology-aware regularization.

    The scorer deliberately prevents a semantically-close but structurally weak / unstable
    decoy from dominating the final context purely through adaptive distance.
    """
    def __init__(self, weights: HybridWeights|None=None):
        self.weights=weights or HybridWeights()

    @staticmethod
    def structural_centrality(nodes, weighted_edges):
        deg=defaultdict(float)
        for a,b,w in weighted_edges:
            strength=max(0.0,1.0-float(w))
            deg[a]+=strength; deg[b]+=strength
        mx=max(deg.values(),default=1.0) or 1.0
        return {n:deg.get(n,0.0)/mx for n in nodes}

    @staticmethod
    def normalize(scores: Dict[str,float], invert=False):
        if not scores:return {}
        vals=list(scores.values()); lo=min(vals); hi=max(vals)
        if hi-lo<1e-12: out={k:1.0 for k in scores}
        else: out={k:(v-lo)/(hi-lo) for k,v in scores.items()}
        return {k:1-v for k,v in out.items()} if invert else out

    def score(self,nodes,weighted_edges,adaptive_distance,persistence=None,drift=None):
        structural=self.structural_centrality(nodes,weighted_edges)
        adaptive=self.normalize(adaptive_distance,invert=True)
        p=self.normalize(persistence or {})
        d=self.normalize(drift or {},invert=True)
        w=self.weights
        rows=[]
        for n in nodes:
            parts={
                "adaptive":adaptive.get(n,0.0),
                "structural":structural.get(n,0.0),
                "persistence":p.get(n,0.0),
                "drift_stability":d.get(n,1.0 if not drift else 0.0),
            }
            topo_support=(parts["structural"]+parts["persistence"]+parts["drift_stability"])/3.0
            # semantic/adaptive relevance is gated by topological support rather than added blindly
            adaptive_effective=parts["adaptive"]*(0.55+0.45*topo_support)
            total=(w.adaptive*adaptive_effective+w.structural*parts["structural"]+
                   w.persistence*parts["persistence"]+w.drift_stability*parts["drift_stability"])
            rows.append({"id":n,"score":total,"components":parts,"topological_support":topo_support})
        return sorted(rows,key=lambda x:x["score"],reverse=True)
