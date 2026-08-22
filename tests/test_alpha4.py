
from pathlib import Path
from self_reorg.closed_loop import SelfReorganizingTopologyRuntime
from self_reorg.policy_bridge import PolicyTopologyBridge
ROOT=Path(__file__).resolve().parents[1]

def fixture():
 r=SelfReorganizingTopologyRuntime()
 r.add("task","task",score=1,distance=0)
 r.add("good","tool",score=.8,distance=.1);r.add("bad","tool",score=.7,distance=.15)
 r.link("task","good","invoke",.8);r.link("task","bad","invoke",.7)
 return r

def test_feedback_strengthens_and_weakens():
 r=fixture();p=r.execute("task",2)["plan"];old_good=r.graph.nodes["good"].score
 out={x["to"]:{"success":x["to"]=="good","reward":1 if x["to"]=="good" else 0} for x in p}
 r.feedback("task",p,out)
 assert r.graph.nodes["good"].score>=old_good and r.graph.nodes["bad"].score<.7

def test_memory_ingest():
 r=fixture();added=r.ingest_memories("task",[{"id":"m1","score":.9,"distance":.1,"metadata":{"importance":.8}}])
 assert "m1" in added and r.graph.nodes["m1"].kind=="memory"

def test_policy_bridge():
 r=fixture();x=PolicyTopologyBridge().apply(r,{"epsilon":.3,"exploration":.8})
 assert .05<=x["prune_threshold"]<=.4 and .55<=x["shortcut_threshold"]<=.95

def test_adaptive_geometry():
 r=fixture();g=r.adaptive_geometry("task");assert 1<=g["p"]<=3 and .05<=g["epsilon"]<=.8

def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/self-reorganizing-graph.js").read_text()
