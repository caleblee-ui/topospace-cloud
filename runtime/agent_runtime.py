from __future__ import annotations
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Dict, Iterable, List, Optional, Sequence, Any

from core.objects import TopoObject
from core.topology.neighborhood import Neighbor
from runtime.adaptive import AdaptivePolicy


@dataclass
class RoutedObject:
    id: str
    type: str
    distance: float
    features: Dict[str, Any]
    metadata: Dict[str, Any]
    contributions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextBundle:
    state_id: str
    objective: str
    epsilon: float
    p: float
    weights: Dict[str, float]
    objects: List[RoutedObject]
    by_type: Dict[str, List[RoutedObject]] = field(default_factory=dict)

    def ids(self) -> List[str]:
        return [o.id for o in self.objects]

    def to_dict(self):
        return asdict(self)


@dataclass
class StateTransition:
    sequence: int
    timestamp: str
    from_state: Optional[str]
    to_state: str
    objective: str
    action: Optional[str]
    epsilon: float
    neighborhood_ids: List[str]


class AgentRuntime:
    """High-level agent-facing API over a TopoSpace instance.

    The runtime deliberately keeps storage and geometry pluggable. It owns
    adaptive neighborhood selection, typed routing, and state-transition traces.
    """

    def __init__(self, space, adaptive_policy: Optional[AdaptivePolicy] = None, geometry=None, store=None, session_id="default"):
        self.space = space
        self.policy = adaptive_policy or AdaptivePolicy()
        self.geometry = geometry
        self.store = store
        self.session_id = session_id
        self._traces: List[StateTransition] = []
        self._current_state_id: Optional[str] = None

    def _rank_distances(self, state: TopoObject, pool: Iterable[TopoObject]) -> List[float]:
        return sorted(
            self.space.distance_fn(state, obj)
            for obj in pool
            if obj.id != state.id
        )

    def _policy_params(self, state: TopoObject, objective: str, pool: Iterable[TopoObject]):
        pool = list(pool)
        distances = self._rank_distances(state, pool)
        epsilon = self.policy.choose_epsilon(distances)
        p = self.policy.choose_p(state=state, objective=objective)
        weights = self.policy.choose_weights(state=state, objective=objective)
        return epsilon, p, weights

    def context(
        self,
        state: TopoObject,
        objective: str = "",
        *,
        object_types: Optional[Sequence[str]] = None,
        min_points: int = 3,
        max_points: int = 32,
        epsilon: Optional[float] = None,
    ) -> ContextBundle:
        pool = list(self.space.objects())
        if object_types:
            allowed = {t.upper() for t in object_types}
            pool = [o for o in pool if o.type.upper() in allowed]

        adaptive_epsilon, p, weights = self._policy_params(state, objective, pool)
        e = adaptive_epsilon if epsilon is None else float(epsilon)

        # Geometry can be externally adaptive; for v0.2 p/weights are exposed
        # as policy metadata while distance_fn remains backward compatible.
        decision = self.geometry.decide(state, objective, []) if self.geometry else None
        if decision is not None:
            e = float(epsilon) if epsilon is not None else decision.epsilon
        neighbors = self._neighborhood_from_pool(state, pool, e, min_points, max_points, decision)
        routed = [
            RoutedObject(
                id=n.obj.id,
                type=n.obj.type,
                distance=float(n.distance),
                features=dict(n.obj.features),
                metadata=dict(n.obj.metadata),
                contributions=(self.geometry.breakdown(state, n.obj, decision=decision) if self.geometry and decision else {}),
            )
            for n in neighbors
        ]
        by_type: Dict[str, List[RoutedObject]] = {}
        for r in routed:
            by_type.setdefault(r.type.upper(), []).append(r)
        return ContextBundle(
            state_id=state.id,
            objective=objective,
            epsilon=e,
            p=p,
            weights=weights,
            objects=routed,
            by_type=by_type,
        )

    def _neighborhood_from_pool(self, state, pool, epsilon, min_points, max_points, decision=None):
        dist = (lambda obj: self.geometry.distance(state, obj, decision=decision)) if self.geometry and decision else (lambda obj: self.space.distance_fn(state, obj))
        ranked = sorted(
            ((dist(obj), obj) for obj in pool if obj.id != state.id),
            key=lambda x: x[0],
        )
        selected = [(d, o) for d, o in ranked if d < epsilon]
        if len(selected) < min_points:
            selected = ranked[:min_points]
        selected = selected[:max_points]
        return [Neighbor(obj=o, distance=d) for d, o in selected]

    def recall(self, state: TopoObject, objective: str = "", **kwargs):
        return self.context(state, objective, object_types=["MEMORY"], **kwargs)

    def route_tools(self, state: TopoObject, objective: str = "", **kwargs):
        return self.context(state, objective, object_types=["TOOL"], **kwargs)

    def route_skills(self, state: TopoObject, objective: str = "", **kwargs):
        return self.context(state, objective, object_types=["SKILL"], **kwargs)

    def route_agents(self, state: TopoObject, objective: str = "", **kwargs):
        return self.context(state, objective, object_types=["AGENT"], **kwargs)

    def trace(
        self,
        state: TopoObject,
        objective: str = "",
        *,
        action: Optional[str] = None,
        epsilon: Optional[float] = None,
        max_points: int = 32,
    ) -> StateTransition:
        bundle = self.context(
            state,
            objective,
            min_points=0,
            max_points=max_points,
            epsilon=epsilon,
        )
        transition = StateTransition(
            sequence=len(self._traces),
            timestamp=datetime.now(timezone.utc).isoformat(),
            from_state=self._current_state_id,
            to_state=state.id,
            objective=objective,
            action=action,
            epsilon=bundle.epsilon,
            neighborhood_ids=bundle.ids(),
        )
        self._traces.append(transition)
        self._current_state_id = state.id
        if self.store is not None:
            self.store.save_trace(self.session_id, transition.sequence, asdict(transition))
        return transition

    def traces(self) -> List[StateTransition]:
        return list(self._traces)

    def export_trace(self) -> List[Dict[str, Any]]:
        return [asdict(t) for t in self._traces]
