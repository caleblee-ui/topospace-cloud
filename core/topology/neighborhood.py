from dataclasses import dataclass
from typing import Iterable, List, Tuple

@dataclass
class Neighbor:
    obj: object
    distance: float


def epsilon_neighborhood(query, objects: Iterable, distance_fn, epsilon: float,
                         min_points: int = 0, max_points: int = 64) -> List[Neighbor]:
    ranked: List[Tuple[float, object]] = sorted(
        ((distance_fn(query, obj), obj) for obj in objects if getattr(obj, 'id', None) != getattr(query, 'id', None)),
        key=lambda x: x[0]
    )
    selected = [(d, o) for d, o in ranked if d < epsilon]
    if len(selected) < min_points:
        selected = ranked[:min_points]
    selected = selected[:max_points]
    return [Neighbor(obj=o, distance=d) for d, o in selected]


def multiscale_neighborhood(query, objects, distance_fn, epsilons, max_points=128):
    return {
        float(e): epsilon_neighborhood(query, objects, distance_fn, float(e), 0, max_points)
        for e in sorted(epsilons)
    }
