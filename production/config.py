
from dataclasses import dataclass, field
from typing import Dict

@dataclass(frozen=True)
class ProductionConfig:
    epsilon: float=.35
    max_context_items: int=48
    max_context_tokens: int=32000
    reserve_output_tokens: int=4000
    max_agents: int=4
    max_tool_calls: int=12
    max_steps: int=8
    drift_threshold: float=.30
    min_relevance: float=.25
    max_drift: float=.45
    fail_open: bool=True
    telemetry_enabled: bool=True
    cache_size: int=2048
