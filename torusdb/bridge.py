
from __future__ import annotations
from production.adaptive_engine import AdaptiveTopoSpaceEngine
from torusdb.models import MemoryRecord

class TorusTopoMemoryBridge:
    """TorusDB stores memory; TopoSpace controls recall visibility."""
    def __init__(self,backend,engine=None):
        self.backend=backend
        self.engine=engine or AdaptiveTopoSpaceEngine()

    def remember(self,record:MemoryRecord):
        return self.backend.upsert(record)

    def forget(self,memory_id):
        return self.backend.delete(memory_id)

    def recall(self,query,limit=50,max_return=12,uncertainty=.3,complexity=.4,cost_pressure=.5):
        memories=self.backend.search(query,limit)
        context=[]
        for m in memories:
            # normalize memory-native signals into TopoSpace production context contract
            context.append({
              "id":m.id,
              "type":"memory",
              "content":m.content,
              "ciphertext":m.ciphertext,
              "metadata":m.metadata,
              "tokens":m.tokens,
              "utility":max(0.01,.55*m.semantic_score+.45*m.importance),
              "distance":m.distance,
              "score":max(m.semantic_score,m.importance),
              "drift":m.drift,
            })
        result=self.engine.optimize_adaptive(
          objective=query,context=context,agents=[],required_capabilities=[],
          uncertainty=uncertainty,complexity=complexity,cost_pressure=cost_pressure)
        kept=result["context"][:max_return]
        return {
          "query":query,
          "memories":kept,
          "candidate_count":len(memories),
          "returned_count":len(kept),
          "context_tokens":result.get("context_tokens",0),
          "adaptive":result.get("adaptive",{}),
          "quality_guard":result.get("quality_guard",{})
        }
