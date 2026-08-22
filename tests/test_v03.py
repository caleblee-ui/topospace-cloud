import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core import TopoObject, TopoSpace
from core.metrics.composite import Component
from core.metrics.adaptive import AdaptiveGeometry
from runtime import AgentRuntime, AdaptivePolicy
from index.sqlite_store import SQLiteObjectStore

def f(name): return lambda a,b: abs(float(a.features.get(name,0))-float(b.features.get(name,0)))
comps={n:Component(n,f(n),1) for n in ['semantic','risk','reliability']}
policy=AdaptivePolicy(default_weights={'semantic':1,'risk':1,'reliability':1})
geom=AdaptiveGeometry(comps,policy)
space=TopoSpace(lambda a,b: geom.distance(a,b,state=a,objective=''))
s=TopoObject('s','STATE',{'semantic':0,'risk':0,'reliability':0})
a=TopoObject('a','TOOL',{'semantic':.1,'risk':.7,'reliability':.3})
b=TopoObject('b','TOOL',{'semantic':.2,'risk':.1,'reliability':.1})
for o in [s,a,b]: space.add(o)
r=AgentRuntime(space,policy,geometry=geom)
normal=r.context(s,'general',min_points=2,max_points=2,epsilon=10)
security=r.context(s,'security auth risk',min_points=2,max_points=2,epsilon=10)
assert normal.p != security.p
assert security.weights['risk'] > normal.weights['risk']
assert security.objects[0].id == 'b'
assert security.objects[0].contributions
with tempfile.TemporaryDirectory() as td:
    st=SQLiteObjectStore(os.path.join(td,'x.db')); st.upsert(a); assert st.get('a').features['risk']==.7
    rr=AgentRuntime(space,policy,geometry=geom,store=st,session_id='test'); rr.trace(s,'security',action='start'); assert len(st.traces('test'))==1; st.close()
print('TopoSpace v0.3 tests: PASS')
