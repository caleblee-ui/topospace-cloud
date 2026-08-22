
from pathlib import Path
from optimization_v2.hierarchy import HierarchicalTopology,TopologyNode
from optimization_v2.hybrid_router import HybridTopologyRouter
from optimization_v2.engine import OptimizationEngineV2
from optimization_v2.consolidation import AdaptiveMemoryConsolidator

ROOT=Path(__file__).resolve().parents[1]

def test_hierarchy():
 h=HierarchicalTopology();x=h.organize([TopologyNode("a",.1),TopologyNode("b",.8)])
 assert x[0][0].id=="a" and x[3][0].id=="b"

def test_hybrid_router_prefers_relevant():
 r=HybridTopologyRouter()
 a={"score":.9,"distance":.1,"utility":.8,"drift":.1}
 b={"score":.2,"distance":.8,"utility":.3,"drift":.1}
 assert r.score(a)>r.score(b)

def test_engine_reduces_context():
 e=OptimizationEngineV2()
 items=[{"id":str(i),"distance":.05 if i<3 else .8,"score":.9 if i<3 else .1,"utility":.9 if i<3 else .2,"tokens":100} for i in range(20)]
 out=e.optimize(items,token_budget=500)
 assert out["context_tokens"]<=500 and out["token_reduction"]>.5

def test_memory_consolidation():
 c=AdaptiveMemoryConsolidator(.5)
 x=c.consolidate([{"id":"a","content":"oauth refresh token"},{"id":"b","content":"oauth refresh token policy"},{"id":"c","content":"button ui"}])
 assert len(x)<3

def test_v2_visual():
 assert "customElements.define" in (ROOT/"web-sdk/optimization-v2-panel.js").read_text()
