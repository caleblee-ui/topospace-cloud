
from model_router13.default_profiles import default_profiles
from model_router13.models import RoutingContext
from routing_policy14.policy import LearnedModelRoutingPolicy
from routing_policy14.models import RoutingOutcome
from routing_policy14.safe_policy import SafeRoutingPolicy
def test_policy_routes():
    assert LearnedModelRoutingPolicy(default_profiles()).route(RoutingContext())["selected"] in {"fast","balanced","reasoning"}
def test_feedback_shifts_high():
    p=LearnedModelRoutingPolicy(default_profiles())
    for _ in range(100):
        p.feedback(RoutingOutcome("reasoning",.99,1000,200,900,.4,True,"high"))
        p.feedback(RoutingOutcome("balanced",.60,1000,200,800,.2,True,"high"))
        p.feedback(RoutingOutcome("fast",.45,1000,200,300,.05,True,"high"))
    assert p.route(RoutingContext(risk=.9))["selected"]=="reasoning"
def test_low_learning():
    p=LearnedModelRoutingPolicy(default_profiles())
    for _ in range(100):
        p.feedback(RoutingOutcome("fast",.98,500,100,250,.03,True,"low"))
        p.feedback(RoutingOutcome("balanced",.65,500,100,600,.15,True,"low"))
        p.feedback(RoutingOutcome("reasoning",.60,500,100,1200,.5,True,"low"))
    assert p.route(RoutingContext(risk=.1,ambiguity=.1,topology_complexity=.1))["selected"]=="fast"
def test_guardrail():
    out=SafeRoutingPolicy(LearnedModelRoutingPolicy(default_profiles()),{"fast"}).route(RoutingContext(risk=.95))
    assert out["selected"]!="fast"
