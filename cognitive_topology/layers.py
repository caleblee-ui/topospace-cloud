
from dataclasses import dataclass,field
import time

@dataclass
class CognitiveMemory:
    id:str
    content:str
    layer:str="working"
    importance:float=.5
    confidence:float=.5
    utility:float=.5
    distance:float=1.0
    access_count:int=0
    success_count:int=0
    created_at:float=field(default_factory=time.time)
    last_accessed:float=field(default_factory=time.time)
    metadata:dict=field(default_factory=dict)

    @property
    def success_rate(self):
        return self.success_count/max(1,self.access_count)

class CognitiveTopologyLayers:
    VALID={"working","episodic","semantic"}
    def __init__(self):
        self.layers={x:{} for x in self.VALID}

    def put(self,memory):
        if memory.layer not in self.VALID:raise ValueError("invalid_cognitive_layer")
        for layer in self.layers.values():layer.pop(memory.id,None)
        self.layers[memory.layer][memory.id]=memory
        return memory

    def get(self,memory_id):
        for layer in self.layers.values():
            if memory_id in layer:return layer[memory_id]
        return None

    def all(self):
        return [m for layer in self.layers.values() for m in layer.values()]

    def counts(self):
        return {k:len(v) for k,v in self.layers.items()}
