
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class AgentNode:
    id: str
    capabilities: List[str]
    adaptive_distance: float
    persistence: float = 0.0
    drift: float = 0.0
    cost: float = 0.0
    risk: float = 0.0
    reliability: float = 1.0
    metadata: Dict[str,Any] = field(default_factory=dict)

@dataclass
class AgentTeam:
    members: List[dict]
    topology_edges: List[tuple]
    objective: str
    score: float
