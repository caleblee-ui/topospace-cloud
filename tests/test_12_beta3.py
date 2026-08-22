
from model_router13.default_profiles import default_profiles
from model_router13.router import TopologyAwareModelRouter
from model_router13.models import RoutingContext

def test_low_complexity_prefers_non_reasoning():
    r=TopologyAwareModelRouter(default_profiles())
    out=r.route(RoutingContext(risk=.1,ambiguity=.1,topology_complexity=.1,latency_pressure=.8,expected_input_tokens=1000))
    assert out["selected"] in {"fast","balanced"}

def test_high_complexity_prefers_reasoning_or_balanced():
    r=TopologyAwareModelRouter(default_profiles())
    out=r.route(RoutingContext(risk=.9,ambiguity=.95,topology_complexity=.95,coupling_strength=.8,expected_tool_calls=6,expected_input_tokens=5000))
    assert out["selected"] in {"reasoning","balanced"}

def test_context_limit_filters():
    r=TopologyAwareModelRouter(default_profiles())
    out=r.route(RoutingContext(expected_input_tokens=150000,ambiguity=.9))
    assert out["selected"]=="reasoning"

def test_feedback_changes_history():
    r=TopologyAwareModelRouter(default_profiles())
    r.feedback("balanced",1,True,600)
    assert r.history.stats("balanced")["success_rate"]==1.0
