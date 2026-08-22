
from dataclasses import dataclass, asdict

@dataclass
class RuntimeSignals:
    success_rate:float=.9
    uncertainty:float=.3
    drift:float=.1
    token_pressure:float=.5
    latency_pressure:float=.3
    tool_failure_rate:float=.0
    memory_hit_rate:float=.7

@dataclass
class AutopilotDecision:
    epsilon:float
    p:float
    max_context_tokens:int
    memory_recall_limit:int
    tool_radius:float
    exploration:float
    reason:list

    def to_dict(self): return asdict(self)
