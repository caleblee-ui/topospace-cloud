
from dataclasses import dataclass, field
from typing import Any, Dict

@dataclass
class ModelUsage:
    input_tokens:int=0
    output_tokens:int=0
    cached_input_tokens:int=0
    cost_usd:float=0.0

@dataclass
class ModelResult:
    text:str
    usage:ModelUsage
    latency_ms:float
    raw:Dict[str,Any]=field(default_factory=dict)

class ModelProvider:
    def generate(self, *, model:str, prompt:str, system:str="", temperature:float=0.0, max_output_tokens:int=2048, **kwargs)->ModelResult:
        raise NotImplementedError
