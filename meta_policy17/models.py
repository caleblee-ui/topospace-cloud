
from dataclasses import dataclass,field

@dataclass
class MetaObjective:
    quality:float
    cost:float
    latency:float
    success:float
    violations:int=0
    instability:float=0.0

@dataclass
class MetaDecision:
    geometry_family:str
    epsilon:float
    p:float
    model:str
    path:str
    score:float
    diagnostics:dict=field(default_factory=dict)
