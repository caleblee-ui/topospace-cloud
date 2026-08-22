
from learned_field.network import CouplingFieldNetwork
from learned_field.models import FieldState
from learned_field.runtime import LearnedTopologicalFieldRuntime
from unified_runtime.models import AgentState
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder

def make(domain):
    out=[]
    for i in range(8):
        good=i<3
        out.append({"id":f"{domain}-{i}","kind":domain,
                    "semantic_distance":.1 if good else .7,
                    "structural_distance":.1 if good else .65,
                    "history_distance":.1 if good else .6,
                    "policy_distance":0 if good else (1 if domain in {"tool","plan"} else 0),
                    "security_distance":0 if good else (1 if domain=="tool" else 0),
                    "cost_distance":.1 if good else .5,
                    "reliability_distance":.1 if good else .6})
    return out

def test_field_changes_with_state():
    n=CouplingFieldNetwork()
    a=n.forward(FieldState(hierarchy=0))
    b=n.forward(FieldState(hierarchy=1))
    assert a.couplings["memory"]["plan"]!=b.couplings["memory"]["plan"]

def test_tool_pressure_changes_tool_skill():
    n=CouplingFieldNetwork()
    a=n.forward(FieldState(tool_pressure=0))
    b=n.forward(FieldState(tool_pressure=1))
    assert b.couplings["tool"]["skill"]>a.couplings["tool"]["skill"]

def test_feedback_updates_field():
    n=CouplingFieldNetwork();s=FieldState(risk=.5)
    before=n.forward(s).couplings["tool"]["plan"]
    after=n.update(s,{"tool":1,"plan":1}).couplings["tool"]["plan"]
    assert before!=after

def test_runtime_integration():
    b=RuntimeSpaceBuilder()
    spaces={d:b.build_space(make(d)) for d in ("memory","tool","skill","plan")}
    s=AgentState("t","x",hierarchy=.8,metadata={"memory_pressure":.6})
    out=LearnedTopologicalFieldRuntime().solve(s,spaces)
    assert "field_snapshot" in out and set(out["routes"])=={"memory","tool","skill","plan"}

def test_constraints_preserved():
    b=RuntimeSpaceBuilder()
    spaces={d:b.build_space(make(d)) for d in ("memory","tool","skill","plan")}
    out=LearnedTopologicalFieldRuntime().solve(AgentState("t","x",risk=.9),spaces)
    bad=[x for x in out["routes"]["tool"]["selected"]
         if x["payload"].get("policy_distance",0)>=1 or x["payload"].get("security_distance",0)>=1]
    assert not bad
