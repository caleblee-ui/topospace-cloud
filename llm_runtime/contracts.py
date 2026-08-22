
from dataclasses import dataclass,field
from typing import Any,Dict,List

@dataclass
class LLMRequest:
    task_id:str
    messages:List[Dict[str,str]]
    model:str="default"
    max_tokens:int=1024
    metadata:Dict[str,Any]=field(default_factory=dict)

@dataclass
class LLMUsage:
    input_tokens:int=0
    output_tokens:int=0
    tool_calls:int=0
    latency_ms:float=0.0
    success:bool=True

@dataclass
class LLMResult:
    text:str
    usage:LLMUsage
    metadata:Dict[str,Any]=field(default_factory=dict)
