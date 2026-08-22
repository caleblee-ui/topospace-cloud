
from dataclasses import dataclass,field
@dataclass
class ExecutionCandidate:
 id:str
 kind:str
 distance:float
 utility:float
 confidence:float
 token_cost:int=0
 latency_ms:float=0
 success_rate:float=.5
 metadata:dict=field(default_factory=dict)
@dataclass
class OptimizationBudget:
 max_tokens:int=4000
 max_tool_calls:int=8
 max_latency_ms:float=10000
 epsilon:float=.5
