
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

@dataclass
class MemoryRecord:
    id:str
    content:Optional[str]=None
    ciphertext:Optional[str]=None
    metadata:Dict[str,Any]=field(default_factory=dict)
    semantic_score:float=0.0
    distance:float=1.0
    importance:float=0.5
    drift:float=0.0
    tokens:int=0

    def payload(self):
        return {
          "id":self.id,"content":self.content,"ciphertext":self.ciphertext,
          "metadata":self.metadata,"semantic_score":self.semantic_score,
          "distance":self.distance,"importance":self.importance,
          "drift":self.drift,"tokens":self.tokens
        }
