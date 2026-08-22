"""Deterministic synthetic benchmark: semantic Top-K vs composite TopoSpace.

This is not a claim about real-world superiority. It is a regression harness that
creates cases where operational relevance depends on non-semantic features too.
"""
import math, os, random, sys, time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core import TopoObject, TopoSpace
from core.metrics.lp import weighted_lp
from runtime import AgentRuntime

R = random.Random(1729)
FEATURES = ["semantic", "structural", "temporal", "risk", "cost", "reliability"]
WEIGHTS = [2.0, 1.7, 0.7, 1.3, 0.5, 1.0]

def vec(o): return [float(o.features[k]) for k in FEATURES]
def dist(a,b): return weighted_lp(vec(a), vec(b), p=1.7, weights=WEIGHTS)
def cosine(a,b):
    dot=sum(x*y for x,y in zip(a,b)); na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(y*y for y in b))
    return dot/(na*nb) if na and nb else 0.0

state = TopoObject("query", "STATE", dict(zip(FEATURES,[.92,.90,.85,.70,.20,.88])))
objects=[]
relevant=set()
# Operationally relevant: close across the composite state, not merely semantic.
for i in range(30):
    vals=[max(0,min(1,v+R.uniform(-.08,.08))) for v in vec(state)]
    oid=f"rel-{i:03d}"; relevant.add(oid); objects.append(TopoObject(oid,"TOOL",dict(zip(FEATURES,vals))))
# Semantic decoys: high semantic coordinate but structurally/risk-wise far.
for i in range(120):
    vals=[R.uniform(.88,1.0),R.uniform(0,.35),R.uniform(.1,.9),R.uniform(0,.25),R.uniform(.65,1),R.uniform(.25,.65)]
    objects.append(TopoObject(f"decoy-{i:03d}","TOOL",dict(zip(FEATURES,vals))))
# Noise
for i in range(350):
    vals=[R.random() for _ in FEATURES]
    objects.append(TopoObject(f"noise-{i:03d}","TOOL",dict(zip(FEATURES,vals))))

k=30
start=time.perf_counter()
# Semantic-only baseline deliberately uses just the semantic dimension as a 1-D embedding proxy.
semantic_rank=sorted(objects,key=lambda o: abs(state.features["semantic"]-o.features["semantic"]))[:k]
base_ms=(time.perf_counter()-start)*1000
base_hits=sum(o.id in relevant for o in semantic_rank)

space=TopoSpace(dist)
for o in objects: space.add(o)
runtime=AgentRuntime(space)
start=time.perf_counter()
topo=runtime.context(state,"secure authentication",min_points=k,max_points=k,epsilon=0.01).objects
topo_ms=(time.perf_counter()-start)*1000
topo_hits=sum(o.id in relevant for o in topo)

print(f"dataset={len(objects)} k={k}")
print(f"semantic_topk recall@{k}={base_hits/len(relevant):.3f} precision@{k}={base_hits/k:.3f} latency_ms={base_ms:.3f}")
print(f"topospace     recall@{k}={topo_hits/len(relevant):.3f} precision@{k}={topo_hits/k:.3f} latency_ms={topo_ms:.3f}")
assert topo_hits >= base_hits
