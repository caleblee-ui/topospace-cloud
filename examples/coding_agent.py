import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core import TopoObject, TopoSpace
from core.metrics.lp import weighted_lp

FEATURES = ['semantic','structural','temporal','risk','cost','reliability']
WEIGHTS = [2.0, 1.7, 0.7, 1.3, 0.5, 1.0]

def vec(o): return [float(o.features[k]) for k in FEATURES]
def dist(a,b): return weighted_lp(vec(a), vec(b), p=1.7, weights=WEIGHTS)

space = TopoSpace(dist)
objs = [
    TopoObject('task.oauth','STATE', dict(zip(FEATURES,[0.90,0.88,0.90,0.70,0.20,0.80]))),
    TopoObject('auth.py','CODE', dict(zip(FEATURES,[0.91,0.92,0.80,0.65,0.10,0.85]))),
    TopoObject('oauth.py','CODE', dict(zip(FEATURES,[0.95,0.90,0.84,0.70,0.10,0.86]))),
    TopoObject('auth_test.py','CODE', dict(zip(FEATURES,[0.80,0.85,0.83,0.55,0.10,0.90]))),
    TopoObject('security-agent','AGENT', dict(zip(FEATURES,[0.82,0.55,0.70,0.92,0.35,0.93]))),
    TopoObject('github.search','TOOL', dict(zip(FEATURES,[0.66,0.44,0.90,0.25,0.20,0.88]))),
    TopoObject('old-payment-bug','MEMORY', dict(zip(FEATURES,[0.22,0.20,0.10,0.40,0.10,0.60]))),
]
for o in objs: space.add(o)
state = space.get('task.oauth')
for n in space.neighborhood(state, epsilon=0.75, min_points=3, max_points=10):
    print(f'{n.obj.id:20s} {n.obj.type:8s} d={n.distance:.4f}')
