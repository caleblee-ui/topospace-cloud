
from pathlib import Path
from optimization_v2.adaptive_metric import DynamicPNorm,AdaptiveEpsilon
from optimization_v2.context_compiler import TopologyContextCompiler
from optimization_v2.topology_cache import TopologyCache
from optimization_v2.incremental import IncrementalNeighborhood
from optimization_v2.adaptive_engine import AdaptiveOptimizationEngine
ROOT=Path(__file__).resolve().parents[1]

def test_dynamic_p():
 p=DynamicPNorm().choose_p([[.1,.1],[.11,.1],[.1,.11]]);assert 1<=p<=3
def test_epsilon():
 e=AdaptiveEpsilon().choose([.1,.2,.3,.4]);assert .05<=e<=.8
def test_compiler_budget():
 c=TopologyContextCompiler().compile("x",[{"id":"a","distance":.1,"score":.9,"tokens":100},{"id":"b","distance":.2,"score":.8,"tokens":500}],200);assert c["context_tokens"]<=200
def test_cache():
 c=TopologyCache();c.set("x",{"a":1});assert c.get("x")["a"]==1
def test_incremental():
 n=IncrementalNeighborhood(.2);n.upsert("a",.1);n.upsert("b",.2);assert "b" in n.get("a")
def test_adaptive_engine_cache():
 e=AdaptiveOptimizationEngine();items=[{"id":"a","distance":.1,"score":.9,"utility":.9,"tokens":100}]
 assert not e.optimize("x",items,200)["cache_hit"]
 assert e.optimize("x",items,200)["cache_hit"]
def test_panel():
 assert "customElements.define" in (ROOT/"web-sdk/adaptive-topology-panel.js").read_text()
