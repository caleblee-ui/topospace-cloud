
from dataclasses import dataclass,field
@dataclass
class RoutingOutcome:
    model:str;quality:float;input_tokens:int;output_tokens:int;latency_ms:float;cost:float;success:bool;topology_bucket:str
    metadata:dict=field(default_factory=dict)
@dataclass
class RoutingWeights:
    quality:float=.60
    cost:float=.10
    latency:float=.10
    success:float=.20
