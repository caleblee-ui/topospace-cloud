
from geometry_policy.model import PolicyState
from geometry_policy.network import GeometryPolicyNetwork
from geometry_policy.compiler import GeometryCompiler
from geometry_policy.controller import AdaptiveGeometryController
from geometry_policy.reward import geometry_reward
from general_geometry.views import ViewValue

def test_high_risk_selects_noncompensatory_geometry():
    p=GeometryPolicyNetwork()
    d=p.decide(PolicyState(risk=1.0,hierarchy=0.0))
    assert d.aggregator in {"chebyshev","nested"}

def test_hierarchy_selects_nested():
    p=GeometryPolicyNetwork()
    d=p.decide(PolicyState(hierarchy=1.0,risk=.2))
    assert d.aggregator=="nested"

def test_decision_bounds():
    d=GeometryPolicyNetwork().decide(PolicyState())
    assert 1<=d.p<=4 and .15<=d.epsilon<=.9
    assert abs(sum(d.weights)-1)<1e-9

def test_compiler_all_families():
    p=GeometryPolicyNetwork()
    c=GeometryCompiler()
    for risk,hier,amb,pressure in [(0,0,1,0),(1,0,0,0),(0,0,0,1),(0,1,0,0)]:
        d=p.decide(PolicyState(risk=risk,hierarchy=hier,ambiguity=amb,candidate_pressure=pressure))
        assert c.compile(d) is not None

def test_reward_penalizes_violation():
    good=geometry_reward(5,6,6,0)
    bad=geometry_reward(5,6,6,1)
    assert good>bad

def test_controller_end_to_end():
    p=GeometryPolicyNetwork()
    ctl=AdaptiveGeometryController(p)
    candidates=[]
    for i in range(5):
        candidates.append({"id":str(i),"views":[ViewValue(str(j),.1+i*.05) for j in range(7)]})
    r=ctl.retrieve(PolicyState(hierarchy=1),candidates)
    assert "decision" in r and "selected" in r

def test_feedback_changes_policy():
    p=GeometryPolicyNetwork()
    s=PolicyState(risk=.8,hierarchy=.8)
    d=p.decide(s)
    before=[row[:] for row in p.family_w.values()]
    p.update(s,d,1.0)
    after=[row[:] for row in p.family_w.values()]
    assert before!=after
