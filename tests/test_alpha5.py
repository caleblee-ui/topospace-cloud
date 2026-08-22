
from pathlib import Path
from cognitive_topology.runtime import TopologicalCognitiveRuntime
ROOT=Path(__file__).resolve().parents[1]

def test_layers_and_consolidation():
 r=TopologicalCognitiveRuntime();r.remember("m","oauth policy",importance=.95,confidence=.95,utility=.95,distance=.1)
 for _ in range(6):r.record_use("m",True,1)
 moved=r.consolidate();assert r.layers.get("m").layer in {"episodic","semantic"} and moved

def test_recall_prefers_semantic():
 r=TopologicalCognitiveRuntime()
 r.remember("a","a",layer="semantic",importance=.9,confidence=.9,utility=.9,distance=.1)
 r.remember("b","b",layer="working",importance=.2,confidence=.2,utility=.2,distance=.8)
 assert r.recall()["memories"][0].id=="a"

def test_torus_import_export():
 r=TopologicalCognitiveRuntime();ids=r.torus.import_records(r.layers,[{"id":"x","content":"memory","importance":.8}])
 assert ids==["x"] and r.torus.export_record(r.layers.get("x"))["id"]=="x"

def test_bind_to_execution_topology():
 r=TopologicalCognitiveRuntime();r.execution.add("task","task",score=1,distance=0)
 r.remember("m","auth",layer="semantic",importance=.9,confidence=.9,utility=.9,distance=.1)
 out=r.bind_recall_to_task("task");assert "m" in r.execution.graph.nodes and out["memories"]

def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/cognitive-topology.js").read_text()
