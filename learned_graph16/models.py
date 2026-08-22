
from dataclasses import dataclass,field
from typing import List

@dataclass
class PathTemplate:
    name:str
    stages:List[str]
    nominal_cost:float
    nominal_latency_ms:float
    risk_floor:float=0.0

@dataclass
class PathOutcome:
    topology_bucket:str
    path_name:str
    reward:float
    success:bool
    cost:float
    latency_ms:float
