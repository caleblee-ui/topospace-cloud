
from dataclasses import dataclass,field
from typing import Dict,List

@dataclass
class DomainGeometryState:
    domain:str
    epsilon:float
    p:float
    aggregator:str
    selected_ids:List[str]=field(default_factory=list)
    influence:Dict[str,float]=field(default_factory=dict)

@dataclass
class JointTopologyState:
    task_id:str
    domains:Dict[str,DomainGeometryState]=field(default_factory=dict)
    iteration:int=0
