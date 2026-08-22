
from pathlib import Path
from collective_topology.runtime import CollectiveTopologyRuntime
from collective_topology.cognitive_bridge import CollectiveCognitiveBridge
from cognitive_topology.runtime import TopologicalCognitiveRuntime
ROOT=Path(__file__).resolve().parents[1]

def test_collective_publish_and_sync():
 r=CollectiveTopologyRuntime()
 r.register_agent("a","t",["security"])
 r.register_agent("b","t",["security"])
 ids=r.publish_success("a",[{"id":"p1","kind":"pattern","tags":["security"],"success_rate":.9,"reward":.9}])
 out=r.sync_agent("b")
 assert ids==["p1"] and "p1" in out["imported"]

def test_tenant_isolation():
 r=CollectiveTopologyRuntime()
 r.register_agent("a","t1",["x"]);r.register_agent("b","t2",["x"])
 r.publish_success("a",[{"id":"p","kind":"pattern","reward":.9,"access_scope":"tenant"}])
 assert "p" not in r.sync_agent("b")["imported"]

def test_specialization_ranking():
 r=CollectiveTopologyRuntime()
 a=r.register_agent("a","t",["security"])
 r.register_agent("s","t",[])
 r.publish_success("s",[{"id":"sec","kind":"pattern","tags":["security"],"reward":.8},{"id":"ui","kind":"pattern","tags":["ui"],"reward":.85}])
 out=r.sync_agent("a",1)
 assert out["selected"][0]=="sec"

def test_cognitive_bridge():
 c=TopologicalCognitiveRuntime()
 c.remember("m","oauth",layer="semantic",importance=.9,confidence=.9,utility=.9,distance=.1,metadata={"tags":["security"]})
 r=CollectiveTopologyRuntime();r.register_agent("a","t",["security"])
 ids=CollectiveCognitiveBridge().publish_semantic("a",c,r)
 assert "semantic:m" in ids

def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/collective-topology.js").read_text()
