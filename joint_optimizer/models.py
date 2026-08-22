
from dataclasses import dataclass,field

@dataclass
class JointObjective:
    task_reward:float
    token_cost:float=0.0
    latency_cost:float=0.0
    violations:int=0
    instability:float=0.0

@dataclass
class JointDecision:
    geometry_family:str
    epsilon:float
    p:float
    field_confidence:float
    aggregate_score:float
    diagnostics:dict=field(default_factory=dict)
