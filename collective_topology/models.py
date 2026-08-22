
from dataclasses import dataclass,field
import time

@dataclass
class AgentTopologyState:
    agent_id:str
    tenant_id:str="default"
    specialization:set=field(default_factory=set)
    local_nodes:dict=field(default_factory=dict)
    local_edges:list=field(default_factory=list)
    updated_at:float=field(default_factory=time.time)

@dataclass
class SharedKnowledge:
    id:str
    kind:str
    payload:dict
    score:float=.5
    source_agent:str|None=None
    tenant_id:str="default"
    access_scope:str="tenant"
