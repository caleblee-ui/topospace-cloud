
from meta_runtime18.service import MetaPolicyProductionRuntime
from meta_runtime18.promotion import MetaPromotionAdapter
from unified_runtime.models import AgentState
from model_router13.models import RoutingContext

def test_live_shadow_decision():
    r=MetaPolicyProductionRuntime()
    out=r.decide(AgentState("t","x"),RoutingContext())
    assert "live" in out and "shadow" in out

def test_shadow_accumulates():
    r=MetaPolicyProductionRuntime()
    for _ in range(10):r.observe(.7,.75,True,0,950)
    assert r.shadow.summary()["samples"]==10

def test_promotion_after_good_challenger():
    r=MetaPolicyProductionRuntime()
    for _ in range(100):r.observe(.70,.75,True,0,980)
    assert MetaPromotionAdapter().check(r)["promote"]

def test_high_risk_meta_guardrail():
    r=MetaPolicyProductionRuntime()
    out=r.decide(AgentState("t","x",risk=.95),RoutingContext(risk=.95))
    assert out["live"]["meta"].model!="fast"
    assert "reasoning" in out["live"]["meta"].path
