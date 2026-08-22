
from __future__ import annotations
import math

class AdaptiveMemoryConsolidator:
    """Produces compact memory representatives without altering source records."""
    def __init__(self,similarity_threshold=.86):
        self.threshold=similarity_threshold

    @staticmethod
    def _tokens(text): return set(str(text).lower().split())

    def similarity(self,a,b):
        x,y=self._tokens(a),self._tokens(b)
        if not x and not y:return 1.0
        return len(x&y)/max(1,len(x|y))

    def consolidate(self,records):
        groups=[]
        for r in records:
            placed=False
            for g in groups:
                if self.similarity(r.get("content",""),g[0].get("content",""))>=self.threshold:
                    g.append(r);placed=True;break
            if not placed:groups.append([r])
        compact=[]
        for g in groups:
            best=max(g,key=lambda x:(x.get("importance",.5),x.get("semantic_score",0)))
            item=dict(best)
            item["consolidated_ids"]=[x.get("id") for x in g]
            item["consolidated_count"]=len(g)
            compact.append(item)
        return compact
