
from dataclasses import dataclass,field
from typing import Dict

@dataclass
class FieldState:
    risk:float=0.0
    ambiguity:float=0.0
    hierarchy:float=0.0
    candidate_pressure:float=0.0
    latency_pressure:float=0.0
    memory_pressure:float=0.0
    tool_pressure:float=0.0

@dataclass
class FieldSnapshot:
    couplings:Dict[str,Dict[str,float]]=field(default_factory=dict)
    confidence:float=0.0
