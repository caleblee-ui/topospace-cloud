"""Repository-shaped benchmark over the TopoSpace source tree itself.

Builds CODE objects from real Python files using dependency/lexical features and asks
for files relevant to 'adaptive geometry context routing'. Ground truth is a small,
explicit architecture label set. This remains a local engineering benchmark, not an
external performance claim.
"""
from __future__ import annotations
import ast, math, os, pathlib, re, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core import TopoObject, TopoSpace
from core.metrics.composite import Component
from core.metrics.adaptive import AdaptiveGeometry
from runtime import AgentRuntime, AdaptivePolicy

ROOT=pathlib.Path(__file__).resolve().parents[1]
QUERY='adaptive geometry context routing state objective epsilon weights p'
TOK=set(re.findall(r'[a-z_]+',QUERY.lower()))
GROUND={'core/metrics/adaptive.py','runtime/adaptive.py','runtime/agent_runtime.py','core/topology/neighborhood.py'}

def scan(path):
    txt=path.read_text(errors='ignore'); rel=str(path.relative_to(ROOT)); words=set(re.findall(r'[a-z_]+',txt.lower()))
    lexical=len(TOK & words)/max(1,len(TOK))
    imports=0; defs=0
    try:
        tree=ast.parse(txt); imports=sum(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(tree)); defs=sum(isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)) for n in ast.walk(tree))
    except SyntaxError: pass
    return TopoObject(rel,'CODE',{
        'semantic':1-lexical,
        'structural': min(1, abs(imports-5)/10),
        'temporal':0.0,
        'risk':0.1 if 'runtime' in rel else 0.3,
        'cost':min(1,len(txt)/20000),
        'reliability':0.1 if ('test' in rel or 'benchmark' in rel) else 0.2,
    },{'lines':txt.count('\n')+1,'imports':imports,'defs':defs})

files=[p for p in ROOT.rglob('*.py') if '__pycache__' not in str(p)]
objs=[scan(p) for p in files]
state=TopoObject('task.repo','STATE',{'semantic':0.0,'structural':0.0,'temporal':0.0,'risk':0.0,'cost':0.0,'reliability':0.0})

def fd(name): return lambda a,b: abs(float(a.features.get(name,0))-float(b.features.get(name,0)))
components={n:Component(n,fd(n),1.0) for n in ['semantic','structural','temporal','risk','cost','reliability']}
policy=AdaptivePolicy(default_weights={'semantic':3.0,'structural':1.0,'temporal':0.1,'risk':0.4,'cost':0.2,'reliability':0.2})
geom=AdaptiveGeometry(components,policy)
space=TopoSpace(lambda a,b: geom.distance(a,b,state=a,objective=QUERY))
for o in objs: space.add(o)
runtime=AgentRuntime(space,policy,geometry=geom)
k=min(6,len(objs))
base=sorted(objs,key=lambda o:o.features['semantic'])[:k]
start=time.perf_counter(); got=runtime.context(state,QUERY,min_points=k,max_points=k,epsilon=0.001).objects; ms=(time.perf_counter()-start)*1000

def metrics(items):
    ids={o.id for o in items}; hits=len(ids & GROUND); return hits/len(GROUND),hits/max(1,len(items))
br,bp=metrics(base); tr,tp=metrics(got)
print('repository_files=',len(objs),'k=',k)
print('semantic', [o.id for o in base], 'recall=',round(br,3),'precision=',round(bp,3))
print('topospace',[o.id for o in got], 'recall=',round(tr,3),'precision=',round(tp,3),'latency_ms=',round(ms,3))
print('adaptive_decision', {'p':runtime.context(state,QUERY,min_points=1,max_points=1).p,'weights':runtime.context(state,QUERY,min_points=1,max_points=1).weights})
