from dataclasses import dataclass, field
from typing import Dict


@dataclass
class AdaptivePolicy:
    base_epsilon: float = 0.5
    density_target: int = 12
    min_epsilon: float = 0.05
    max_epsilon: float = 2.0
    base_p: float = 1.7
    default_weights: Dict[str, float] = field(default_factory=lambda: {
        "semantic": 2.0,
        "structural": 1.7,
        "temporal": 0.7,
        "risk": 1.3,
        "cost": 0.5,
        "reliability": 1.0,
    })

    def choose_epsilon(self, distances):
        if not distances:
            return self.base_epsilon
        ds = sorted(float(d) for d in distances)
        idx = min(max(self.density_target - 1, 0), len(ds)-1)
        e = ds[idx] * 1.001
        return max(self.min_epsilon, min(self.max_epsilon, e))

    def choose_p(self, state=None, objective: str = "") -> float:
        text = (objective or "").lower()
        # Lightweight deterministic policy for v0.2. This is intentionally
        # replaceable by a learned policy in v0.3.
        if any(k in text for k in ("security", "risk", "permission", "auth")):
            return 1.5
        if any(k in text for k in ("optimize", "performance", "latency")):
            return 2.0
        return self.base_p

    def choose_weights(self, state=None, objective: str = "") -> Dict[str, float]:
        weights = dict(self.default_weights)
        text = (objective or "").lower()
        if any(k in text for k in ("security", "risk", "permission", "auth")):
            weights["risk"] *= 1.6
            weights["reliability"] *= 1.25
        if any(k in text for k in ("performance", "latency", "cost")):
            weights["cost"] *= 1.5
            weights["temporal"] *= 1.2
        return weights
