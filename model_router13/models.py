
from dataclasses import dataclass,field

@dataclass
class ModelProfile:
    name:str
    quality:float
    latency_ms:float
    input_cost_per_1k:float
    output_cost_per_1k:float
    tool_affinity:float=.5
    reasoning_affinity:float=.5
    max_context:int=128000
    metadata:dict=field(default_factory=dict)

@dataclass
class RoutingContext:
    risk:float=0.0
    ambiguity:float=0.0
    topology_complexity:float=0.0
    coupling_strength:float=0.0
    candidate_pressure:float=0.0
    latency_pressure:float=0.0
    expected_input_tokens:int=0
    expected_output_tokens:int=512
    expected_tool_calls:int=0
