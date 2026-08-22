import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core import TopoObject, TopoSpace
from core.metrics.composite import Component
from core.metrics.adaptive import AdaptiveGeometry
from runtime import AgentRuntime, AdaptivePolicy

FEATURES=['semantic','structural','temporal','risk','cost','reliability']
def fd(name): return lambda a,b: abs(float(a.features.get(name,0))-float(b.features.get(name,0)))
policy=AdaptivePolicy()
components={n:Component(n,fd(n),1.0) for n in FEATURES}
geometry=AdaptiveGeometry(components,policy)
space=TopoSpace(lambda a,b: geometry.distance(a,b,state=a,objective=''))
for obj in [
TopoObject('task.oauth','STATE',dict(zip(FEATURES,[.90,.88,.90,.70,.20,.80]))),
TopoObject('auth.py','CODE',dict(zip(FEATURES,[.91,.92,.80,.65,.10,.85]))),
TopoObject('oauth.py','CODE',dict(zip(FEATURES,[.95,.90,.84,.70,.10,.86]))),
TopoObject('auth_test.py','CODE',dict(zip(FEATURES,[.80,.85,.83,.55,.10,.90]))),
TopoObject('security-agent','AGENT',dict(zip(FEATURES,[.82,.55,.70,.92,.35,.93]))),
TopoObject('github.search','TOOL',dict(zip(FEATURES,[.66,.44,.90,.25,.20,.88]))),
TopoObject('oauth-docs','MEMORY',dict(zip(FEATURES,[.84,.62,.74,.58,.10,.82]))),
TopoObject('test.run','SKILL',dict(zip(FEATURES,[.74,.84,.90,.30,.15,.95]))),]: space.add(obj)
runtime=AgentRuntime(space,policy,geometry=geometry)
state=space.get('task.oauth'); objective='implement secure OAuth authentication and keep tests passing'
ctx=runtime.context(state,objective,min_points=4,max_points=8)
print('CONTEXT',ctx.ids()); print('EPSILON',round(ctx.epsilon,4),'P',ctx.p,'WEIGHTS',ctx.weights)
print('CONTRIBUTIONS',ctx.objects[0].contributions)
print('TOOLS',runtime.route_tools(state,objective,min_points=0).ids()); print('SKILLS',runtime.route_skills(state,objective,min_points=0).ids()); print('AGENTS',runtime.route_agents(state,objective,min_points=0).ids()); print('MEMORY',runtime.recall(state,objective,min_points=0).ids())
runtime.trace(state,objective,action='task_received'); print('TRACE',runtime.export_trace())
