
from meta_policy17.runtime import MetaPolicyRuntime
from meta_policy17.safety import MetaPolicyGuardrail
from unified_runtime.models import AgentState
from model_router13.models import RoutingContext

def test_meta_decision_has_all_layers():
    r=MetaPolicyRuntime()
    d=r.decide(AgentState("t","x"),RoutingContext())
    assert d["meta"].geometry_family and d["meta"].model and d["meta"].path

def test_feedback_updates():
    r=MetaPolicyRuntime();s=AgentState("t","x",risk=.6);c=RoutingContext(risk=.6)
    d=r.decide(s,c)
    out=r.feedback(d,c,.9,.2,600,True)
    assert "meta_score" in out

def test_high_risk_guardrail():
    r=MetaPolicyRuntime();s=AgentState("t","x",risk=.95);c=RoutingContext(risk=.95)
    d=MetaPolicyGuardrail().apply(s,r.decide(s,c))
    assert d["meta"].model!="fast"
    assert "reasoning" in d["meta"].path

def test_meta_score_reasonable():
    r=MetaPolicyRuntime();d=r.decide(AgentState("t","x"),RoutingContext())
    assert 0<=d["meta"].score<=1
