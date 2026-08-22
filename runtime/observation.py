
from __future__ import annotations
from dataclasses import dataclass, asdict

@dataclass
class AgentObservation:
    success: bool
    message: str = ""
    token_cost_norm: float = 0.0
    latency_norm: float = 0.0
    tool_calls_norm: float = 0.0
    risk: float = 0.0
    discovered_nodes: list = None
    discovered_edges: list = None

    def to_dict(self):
        d=asdict(self)
        d["discovered_nodes"]=d["discovered_nodes"] or []
        d["discovered_edges"]=d["discovered_edges"] or []
        return d
