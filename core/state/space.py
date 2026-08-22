from typing import Dict, Iterable, Optional
from core.objects import TopoObject
from core.topology.neighborhood import epsilon_neighborhood, multiscale_neighborhood

class TopoSpace:
    def __init__(self, distance_fn):
        self.distance_fn = distance_fn
        self._objects: Dict[str, TopoObject] = {}

    def add(self, obj: TopoObject):
        self._objects[obj.id] = obj
        return obj

    def get(self, object_id: str) -> Optional[TopoObject]:
        return self._objects.get(object_id)

    def objects(self, type: Optional[str] = None) -> Iterable[TopoObject]:
        vals = self._objects.values()
        return [o for o in vals if type is None or o.type == type]

    def neighborhood(self, state: TopoObject, epsilon=0.5, min_points=3, max_points=32, type=None):
        pool = self.objects(type=type)
        return epsilon_neighborhood(state, pool, self.distance_fn, epsilon, min_points, max_points)

    def filtration(self, state: TopoObject, epsilons=(0.2,0.4,0.8), max_points=128):
        return multiscale_neighborhood(state, self.objects(), self.distance_fn, epsilons, max_points)
