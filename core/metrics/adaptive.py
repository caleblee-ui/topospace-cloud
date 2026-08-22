from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Any, Optional

from core.metrics.composite import CompositeLpGeometry


@dataclass(frozen=True)
class GeometryDecision:
    p: float
    weights: Dict[str, float]
    epsilon: float
    objective: str = ""


class AdaptiveGeometry:
    """Task/state conditioned Composite Lp geometry.

    Components define normalized dissimilarities D_j(x,y). The policy supplies
    p and per-component weights for each query. No global geometry mutation is
    required, so concurrent callers can use different objectives safely.
    """

    def __init__(self, components, policy):
        self.components = components
        self.policy = policy

    def decide(self, state, objective: str, candidate_distances=None) -> GeometryDecision:
        p = float(self.policy.choose_p(state=state, objective=objective))
        weights = self.policy.choose_weights(state=state, objective=objective)
        epsilon = float(self.policy.choose_epsilon(candidate_distances or []))
        return GeometryDecision(p=p, weights=weights, epsilon=epsilon, objective=objective)

    def distance(self, x, y, *, decision: Optional[GeometryDecision] = None,
                 state=None, objective: str = "") -> float:
        if decision is None:
            decision = self.decide(state or x, objective, [])
        total = 0.0
        for name, comp in self.components.items():
            d = max(0.0, float(comp.fn(x, y)))
            w = max(0.0, float(decision.weights.get(name, comp.weight)))
            total += w * (d ** decision.p)
        return total ** (1.0 / decision.p) if total else 0.0

    def breakdown(self, x, y, *, decision: GeometryDecision) -> Dict[str, Dict[str, float]]:
        out: Dict[str, Dict[str, float]] = {}
        denom = 0.0
        raw_terms = {}
        for name, comp in self.components.items():
            d = max(0.0, float(comp.fn(x, y)))
            w = max(0.0, float(decision.weights.get(name, comp.weight)))
            term = w * (d ** decision.p)
            raw_terms[name] = (d, w, term)
            denom += term
        for name, (d, w, term) in raw_terms.items():
            out[name] = {
                "distance": d,
                "weight": w,
                "lp_term": term,
                "share": (term / denom) if denom else 0.0,
            }
        return out
