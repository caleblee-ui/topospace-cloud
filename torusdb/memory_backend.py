
from __future__ import annotations
from torusdb.backend import TorusMemoryBackend
from torusdb.models import MemoryRecord

class InMemoryTorusBackend(TorusMemoryBackend):
    """Reference backend used for regression tests. Replace with TorusDB adapter in deployment."""
    def __init__(self): self.data={}

    def upsert(self,record):
        self.data[record.id]=record
        return record

    def get(self,memory_id): return self.data.get(memory_id)

    def delete(self,memory_id): return self.data.pop(memory_id,None) is not None

    def search(self,query,limit=50,filters=None):
        q=set((query or "").lower().split())
        rows=[]
        for r in self.data.values():
            text=(r.content or "")+" "+jsonish(r.metadata)
            terms=set(text.lower().split())
            sem=len(q&terms)/max(1,len(q))
            rr=MemoryRecord(**r.payload())
            rr.semantic_score=max(rr.semantic_score,sem)
            rr.distance=min(rr.distance,1-sem)
            rows.append(rr)
        return sorted(rows,key=lambda x:(x.distance,-x.importance))[:limit]

def jsonish(x):
    try:
        import json
        return json.dumps(x,sort_keys=True)
    except Exception:return str(x)
