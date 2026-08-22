
from unified_runtime.models import AgentState
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder
from coupled_geometry.runtime import CrossDomainGeometryRuntime
from coupled_geometry.execution import CoupledExecutionComposer
from coupled_geometry.feedback import CoupledFeedbackLearner

def make(domain,n=10):
    out=[]
    for i in range(n):
        good=i<3
        out.append({
          "id":f"{domain}-{i}","kind":domain,
          "semantic_distance":.08 if good else .65,
          "structural_distance":.10 if good else .6,
          "history_distance":.12 if good else .55,
          "policy_distance":0 if good else (1 if domain in {"tool","plan"} else 0),
          "security_distance":0 if good else (1 if domain=="tool" else 0),
          "cost_distance":.1 if good else .5,
          "reliability_distance":.1 if good else .55
        })
    return out

def test_joint_runtime_solves_all_domains():
    b=RuntimeSpaceBuilder()
    spaces={d:b.build_space(make(d)) for d in ("memory","tool","skill","plan")}
    s=AgentState("t","x",risk=.5,ambiguity=.7,hierarchy=.5)
    out=CrossDomainGeometryRuntime().solve(s,spaces)
    assert set(out["routes"])=={"memory","tool","skill","plan"}
    assert out["joint_state"].iteration>=1

def test_memory_influences_plan():
    r=CrossDomainGeometryRuntime()
    assert r.coupling.matrix["memory"]["plan"]>0

def test_constraints_survive_coupling():
    b=RuntimeSpaceBuilder()
    spaces={d:b.build_space(make(d)) for d in ("memory","tool","skill","plan")}
    s=AgentState("t","x",risk=.2)
    out=CrossDomainGeometryRuntime().solve(s,spaces)
    bad=[x for x in out["routes"]["tool"]["selected"]
         if x["payload"].get("policy_distance",0)>=1 or x["payload"].get("security_distance",0)>=1]
    assert bad==[]

def test_execution_bundle():
    b=RuntimeSpaceBuilder()
    spaces={d:b.build_space(make(d)) for d in ("memory","tool","skill","plan")}
    out=CrossDomainGeometryRuntime().solve(AgentState("t","x"),spaces)
    bundle=CoupledExecutionComposer().compose(out)
    assert bundle["execution_bundle"]

def test_coupling_feedback_updates():
    r=CrossDomainGeometryRuntime()
    before=r.coupling.matrix["memory"]["plan"]
    CoupledFeedbackLearner(r.coupling).update({"memory":1,"plan":1})
    assert r.coupling.matrix["memory"]["plan"]>before
