
from dataclasses import dataclass,field

@dataclass
class PolicySnapshot:
    name:str
    version:int
    reward:float=0.0
    success_rate:float=0.0
    violation_rate:float=0.0
    latency_ms:float=0.0
    sample_count:int=0
    metadata:dict=field(default_factory=dict)

@dataclass
class RolloutState:
    champion:str
    challenger:str|None=None
    stage_percent:int=0
    status:str="stable"
