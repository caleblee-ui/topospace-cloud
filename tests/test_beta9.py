
from joint_optimizer.controller import JointGeometryController
from joint_optimizer.objective import JointUtility
from joint_optimizer.models import JointObjective
from joint_optimizer.stability import GeometryStabilityMonitor
from unified_runtime.models import AgentState

def test_joint_decision_contains_both_layers():
    c=JointGeometryController()
    d=c.decide(AgentState("t","x",risk=.5,hierarchy=.6))
    assert "geometry" in d and "field" in d and "joint" in d

def test_joint_objective_penalizes_violation():
    u=JointUtility()
    good=u.score(JointObjective(1,0,0,0,0))
    bad=u.score(JointObjective(1,0,0,1,0))
    assert good>bad

def test_joint_update_changes_models():
    c=JointGeometryController()
    s=AgentState("t","x",risk=.8,hierarchy=.8)
    d=c.decide(s)
    before=c.field.forward(d["field_state"]).couplings["memory"]["plan"]
    c.update(d,{"memory":1,"plan":1,"tool":.8,"skill":.8},1.0)
    after=c.field.forward(d["field_state"]).couplings["memory"]["plan"]
    assert before!=after

def test_stability_monitor():
    c=JointGeometryController();m=GeometryStabilityMonitor()
    s=AgentState("t","x")
    a=c.decide(s);b=c.decide(s)
    assert m.distance(a,b)>=0
