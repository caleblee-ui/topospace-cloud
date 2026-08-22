
from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class GeometryDecision:
    aggregator: str
    weights: List[float]
    epsilon: float
    p: float = 2.0
    confidence: float = 0.0
    scores: Dict[str,float] = field(default_factory=dict)

@dataclass
class PolicyState:
    task_type: str = "general"
    risk: float = 0.0
    ambiguity: float = 0.0
    hierarchy: float = 0.0
    candidate_pressure: float = 0.0
    latency_pressure: float = 0.0
