
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any
from learning.topology_learner import TopologyLearner, TopologyParams

@dataclass
class ObjectiveWeights:
    success: float = 1.0
    token_cost: float = 0.15
    latency: float = 0.10
    tool_calls: float = 0.08
    risk: float = 0.20

class MultiObjectiveTopologyLearner:
    """Wraps TopologyLearner with a normalized multi-objective reward."""

    def __init__(self, base: TopologyLearner|None=None, objectives: ObjectiveWeights|None=None):
        self.base = base or TopologyLearner()
        self.objectives = objectives or ObjectiveWeights()

    @staticmethod
    def _clip01(x):
        return max(0.0, min(1.0, float(x)))

    def reward(self, metrics: Dict[str, Any]) -> float:
        # Expected normalized inputs:
        # success in [0,1], token_cost_norm/latency_norm/tool_calls_norm/risk in [0,1]
        o = self.objectives
        success = self._clip01(metrics.get("success", 0.0))
        token = self._clip01(metrics.get("token_cost_norm", 0.0))
        latency = self._clip01(metrics.get("latency_norm", 0.0))
        calls = self._clip01(metrics.get("tool_calls_norm", 0.0))
        risk = self._clip01(metrics.get("risk", 0.0))
        raw = (
            o.success*success
            - o.token_cost*token
            - o.latency*latency
            - o.tool_calls*calls
            - o.risk*risk
        )
        denom = max(1e-9, o.success + o.token_cost + o.latency + o.tool_calls + o.risk)
        return max(-1.0, min(1.0, raw/denom))

    def update(self, candidate: TopologyParams, metrics: Dict[str, Any]):
        r = self.reward(metrics)
        params = self.base.update(candidate, r)
        return params, r
