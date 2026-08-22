
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Tuple
import math, random, json

@dataclass
class TopologyParams:
    p: float = 2.0
    epsilon: float = 0.35
    weights: Dict[str, float] = field(default_factory=lambda: {
        "semantic": 1.0,
        "structural": 1.0,
        "temporal": 0.2,
        "risk": 0.4,
        "cost": 0.2,
        "reliability": 0.6,
        "path": 1.0,
        "symbol": 1.2,
    })

    def normalized(self):
        s = sum(max(0.0, v) for v in self.weights.values()) or 1.0
        return {k: max(0.0, v)/s for k,v in self.weights.items()}

class TopologyLearner:
    """Small online learner for TopoSpace parameters.

    This is intentionally lightweight: a policy-gradient-like perturb/update loop
    learns p, epsilon and feature weights from downstream task reward.
    """
    def __init__(self, params: TopologyParams|None=None, lr: float = 0.08, seed: int = 7):
        self.params = params or TopologyParams()
        self.lr = lr
        self.rng = random.Random(seed)
        self.history: List[dict] = []

    def propose(self, scale: float = 0.12) -> TopologyParams:
        w = {}
        for k,v in self.params.weights.items():
            w[k] = max(0.01, v * (1.0 + self.rng.uniform(-scale, scale)))
        p = min(4.0, max(1.05, self.params.p + self.rng.uniform(-0.25, 0.25)))
        epsilon = min(0.95, max(0.05, self.params.epsilon + self.rng.uniform(-0.08, 0.08)))
        return TopologyParams(p=p, epsilon=epsilon, weights=w)

    def update(self, candidate: TopologyParams, reward: float):
        reward = max(-1.0, min(1.0, float(reward)))
        a = self.lr * reward
        self.params.p = min(4.0, max(1.05, self.params.p + a*(candidate.p-self.params.p)))
        self.params.epsilon = min(0.95, max(0.05, self.params.epsilon + a*(candidate.epsilon-self.params.epsilon)))
        for k in self.params.weights:
            cv = candidate.weights.get(k, self.params.weights[k])
            self.params.weights[k] = max(0.01, self.params.weights[k] + a*(cv-self.params.weights[k]))
        self.history.append({
            "reward": reward,
            "candidate": {"p": candidate.p, "epsilon": candidate.epsilon, "weights": candidate.weights},
            "current": {"p": self.params.p, "epsilon": self.params.epsilon, "weights": dict(self.params.weights)}
        })
        return self.params

    def state_dict(self):
        return {
            "params": {"p": self.params.p, "epsilon": self.params.epsilon, "weights": dict(self.params.weights)},
            "history": list(self.history),
        }

    def save(self, path):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.state_dict(), f, indent=2)
