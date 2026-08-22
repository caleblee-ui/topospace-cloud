
from pathlib import Path
from dynamic_topology.graph import DynamicAgentTopology,RuntimeNode
from dynamic_topology.runtime import DynamicTopologyRuntime
from dynamic_topology.explain import GraphDecisionExplainer
ROOT=Path(__file__).resolve().parents[1]

def fixture():
 r=DynamicTopologyRuntime();r.add("task","task",score=1,distance=0)
 r.add("m","memory",score=.9,distance=.1);r.add("tool","tool",score=.85,distance=.15);r.add("agent","agent",score=.8,distance=.2)
 r.link("task","m","recall",.9);r.link("task","tool","requires",.8);r.link("task","agent","delegate",.8);return r
def test_graph_neighbors():
 r=fixture();assert len(r.graph.neighbors("task"))==3
def test_plan():
 r=fixture();p=r.execute_plan("task")["plan"];assert p and p[0]["to"] in {"m","tool","agent"}
def test_outcome_updates():
 r=fixture();before=r.graph.nodes["agent"].score;r.update_outcome("agent",True,1);assert r.graph.nodes["agent"].score>before
def test_explain():
 r=fixture();s=r.execute_plan("task")["plan"][0];assert "summary" in GraphDecisionExplainer().explain_step(s)
def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/dynamic-topology-graph.js").read_text()
