
from dataclasses import dataclass,field
from typing import List,Dict,Any
from agent_gateway.contracts import GatewayRequest

@dataclass
class ChatCompletionRequest:
    messages:List[Dict[str,str]]
    model:str="auto"
    max_tokens:int=1024
    metadata:Dict[str,Any]=field(default_factory=dict)

def to_gateway(task_id,req,state=None):
    return GatewayRequest(task_id,req.messages,model=req.model,max_tokens=req.max_tokens,state=state or {},metadata=req.metadata)
