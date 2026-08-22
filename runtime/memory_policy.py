
from __future__ import annotations
class MemoryRetentionPolicy:
    """Topology-aware keep/evict policy for agent memory."""
    def decide(self, memory_rows, keep_threshold=.45, max_keep=50):
        ranked=sorted(memory_rows,key=lambda x:x.get("score",0),reverse=True)
        keep=[x for x in ranked if x.get("score",0)>=keep_threshold][:max_keep]
        keep_ids={x["id"] for x in keep}
        evict=[x for x in memory_rows if x["id"] not in keep_ids]
        return {"keep":keep,"evict":evict}
