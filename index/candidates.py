from __future__ import annotations
from typing import Iterable, List
from core.objects import TopoObject

class CandidateIndex:
    def candidates(self, state: TopoObject, objects: Iterable[TopoObject], limit: int=256) -> List[TopoObject]:
        raise NotImplementedError

class ExactCandidateIndex(CandidateIndex):
    def candidates(self, state, objects, limit=256):
        vals=[o for o in objects if o.id != state.id]
        return vals[:limit] if limit else vals

class SemanticCandidateIndex(CandidateIndex):
    """Dependency-free cosine prefilter when features['semantic_vector'] exists."""
    @staticmethod
    def _cos(a,b):
        import math
        if not a or not b or len(a)!=len(b): return -1.0
        dot=sum(float(x)*float(y) for x,y in zip(a,b)); na=math.sqrt(sum(float(x)**2 for x in a)); nb=math.sqrt(sum(float(y)**2 for y in b))
        return dot/(na*nb) if na and nb else -1.0
    def candidates(self,state,objects,limit=256):
        q=state.features.get('semantic_vector')
        vals=[o for o in objects if o.id != state.id]
        if q is None: return vals[:limit]
        vals.sort(key=lambda o:self._cos(q,o.features.get('semantic_vector')),reverse=True)
        return vals[:limit]
