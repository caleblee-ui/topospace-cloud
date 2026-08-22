
from __future__ import annotations
class IncrementalNeighborhood:
    """Maintains local membership without rebuilding the full space."""
    def __init__(self,epsilon=.35,min_score=.25,max_drift=.45):
        self.epsilon=epsilon;self.min_score=min_score;self.max_drift=max_drift
        self.members={}

    def qualifies(self,obj):
        return (float(obj.get("distance",1))<=self.epsilon and
                float(obj.get("score",0))>=self.min_score and
                float(obj.get("drift",0))<=self.max_drift)

    def rebuild(self,objects):
        self.members={x["id"]:x for x in objects if self.qualifies(x)}
        return list(self.members.values())

    def apply_delta(self,added=None,updated=None,removed=None):
        for nid in removed or []: self.members.pop(nid,None)
        for obj in (added or [])+(updated or []):
            if self.qualifies(obj): self.members[obj["id"]]=obj
            else:self.members.pop(obj["id"],None)
        return list(self.members.values())
