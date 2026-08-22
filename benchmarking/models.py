
from dataclasses import dataclass, asdict, field
from typing import Dict, Any

@dataclass
class BenchmarkTask:
    id:str
    prompt:str
    workload:str
    metadata:Dict[str,Any]=field(default_factory=dict)

@dataclass
class RunRecord:
    task_id:str
    mode:str
    run_index:int
    success:bool
    input_tokens:int
    output_tokens:int
    tool_calls:int
    agent_invocations:int
    latency_ms:float
    cost_usd:float
    extra:Dict[str,Any]=field(default_factory=dict)

    def to_dict(self): return asdict(self)
