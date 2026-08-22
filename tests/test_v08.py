
from topology.simplicial import VietorisRipsComplex
from topology.homology import betti_numbers
from topology.persistent_homology import PersistentHomologySummary
from planning.topological_planner import TopologicalPlanner
from runtime.persistent_agent_context import PersistentAgentContext

def test_vr_complex_triangle():
    s=VietorisRipsComplex().build(["a","b","c"],[("a","b",.1),("b","c",.1),("a","c",.1)],.2)
    assert any(len(x.vertices)==3 for x in s)

def test_betti_cycle_and_fill():
    nodes=["a","b","c"]
    # at .15 all three edges and triangle appear, cycle is filled => beta1=0
    b=betti_numbers(nodes,[("a","b",.1),("b","c",.1),("a","c",.1)],.15)
    assert b["beta0"]==1 and b["beta1"]==0 and b["triangles"]==1

def test_h1_square_cycle():
    nodes=["a","b","c","d"]
    edges=[("a","b",.1),("b","c",.1),("c","d",.1),("d","a",.1)]
    b=betti_numbers(nodes,edges,.2)
    assert b["beta1"]==1

def test_persistent_summary():
    ph=PersistentHomologySummary()
    s=ph.compute(["a","b"],[("a","b",.2)],[.1,.3])
    assert s[0]["beta0"]==2 and s[1]["beta0"]==1

def test_topological_planner_prefers_persistent_low_risk_path():
    adj={"s":[("a",1),("b",1)],"a":[("g",1)],"b":[("g",1)],"g":[]}
    meta={"a":{"risk":.8,"persistence":.1},"b":{"risk":.1,"persistence":.8}}
    r=TopologicalPlanner().plan("s","g",adj,meta)
    assert r.path==["s","b","g"]

def test_persistent_agent_context():
    c=PersistentAgentContext().build(["a","b","c"],[("a","b",.1),("b","c",.4)],[.1,.2,.5])
    assert "ranking" in c and "homology" in c
