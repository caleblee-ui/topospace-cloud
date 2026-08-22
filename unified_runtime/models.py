
from dataclasses import dataclass,field

@dataclass
class AgentState:
    task_id:str
    objective:str
    risk:float=0.0
    ambiguity:float=0.0
    hierarchy:float=0.0
    candidate_pressure:float=0.0
    latency_pressure:float=0.0
    metadata:dict=field(default_factory=dict)

@dataclass
class RuntimeOutcome:
    success:bool
    reward:float
    token_cost:int=0
    latency_ms:float=0.0
    violations:int=0
