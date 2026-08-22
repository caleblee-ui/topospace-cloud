
from dataclasses import dataclass,field
from typing import List,Dict

@dataclass
class ExecutionNode:
    id:str
    kind:str
    model:str|None=None
    expected_cost:float=0.0
    expected_latency_ms:float=0.0
    success_prob:float=.5
    metadata:Dict=field(default_factory=dict)

@dataclass
class ExecutionEdge:
    source:str
    target:str
    condition:str="always"
    weight:float=1.0

@dataclass
class ExecutionGraph:
    nodes:List[ExecutionNode]=field(default_factory=list)
    edges:List[ExecutionEdge]=field(default_factory=list)
    entrypoint:str|None=None
