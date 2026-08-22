
from dataclasses import dataclass,field
from typing import Any,Dict,List,Optional

@dataclass
class GatewayRequest:
    task_id:str
    messages:List[Dict[str,str]]
    model:str="auto"
    max_tokens:int=1024
    tools:List[Dict[str,Any]]=field(default_factory=list)
    memory:List[Dict[str,Any]]=field(default_factory=list)
    skills:List[Dict[str,Any]]=field(default_factory=list)
    plans:List[Dict[str,Any]]=field(default_factory=list)
    state:Dict[str,Any]=field(default_factory=dict)
    metadata:Dict[str,Any]=field(default_factory=dict)

@dataclass
class GatewayDecision:
    model:str
    token_budget:int
    selected_memory:List[str]=field(default_factory=list)
    selected_tools:List[str]=field(default_factory=list)
    selected_skills:List[str]=field(default_factory=list)
    selected_plans:List[str]=field(default_factory=list)
    diagnostics:Dict[str,Any]=field(default_factory=dict)
