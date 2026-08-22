from dataclasses import dataclass
from typing import Callable, Dict, Any

DistanceFn = Callable[[Any, Any], float]

@dataclass
class Component:
    name: str
    fn: DistanceFn
    weight: float = 1.0

class CompositeLpGeometry:
    def __init__(self, components: Dict[str, Component], p: float = 2.0):
        if p < 1:
            raise ValueError('p must be >= 1')
        self.components = components
        self.p = p

    def distance(self, x, y, context=None) -> float:
        terms = []
        for comp in self.components.values():
            d = max(0.0, float(comp.fn(x, y)))
            terms.append(comp.weight * (d ** self.p))
        return sum(terms) ** (1.0 / self.p)

    def breakdown(self, x, y) -> Dict[str, float]:
        return {name: max(0.0, float(comp.fn(x, y))) for name, comp in self.components.items()}
