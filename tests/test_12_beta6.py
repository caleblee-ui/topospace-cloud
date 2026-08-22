
from learned_graph16.templates import default_path_templates
from learned_graph16.policy import LearnedExecutionGraphPolicy
from learned_graph16.models import PathOutcome
from learned_graph16.compiler import LearnedPathCompiler
from learned_graph16.safe_policy import SafeExecutionGraphPolicy
from model_router13.models import RoutingContext

def test_policy_routes():
    p=LearnedExecutionGraphPolicy(default_path_templates())
    assert p.route(RoutingContext())["selected"]

def test_learning_low_prefers_fast():
    p=LearnedExecutionGraphPolicy(default_path_templates())
    for _ in range(100):
        p.feedback(PathOutcome("low","fast_only",.98,True,1,300))
        p.feedback(PathOutcome("low","balanced_tool",.7,True,4,900))
    assert p.route(RoutingContext(risk=.1,ambiguity=.1,topology_complexity=.1))["selected"]=="fast_only"

def test_learning_high_prefers_reasoning_path():
    p=LearnedExecutionGraphPolicy(default_path_templates())
    for _ in range(100):
        p.feedback(PathOutcome("high","memory_balanced_reasoning",.99,True,10,1900))
        p.feedback(PathOutcome("high","fast_tool",.5,False,1.5,500))
    out=p.route(RoutingContext(risk=.9,ambiguity=.9,topology_complexity=.9))
    assert "reasoning" in next(x["stages"] for x in out["ranking"] if x["path"]==out["selected"])

def test_compiler():
    t=default_path_templates()[1]
    g=LearnedPathCompiler().compile(t)
    assert len(g.nodes)==2 and len(g.edges)==1

def test_high_risk_guardrail():
    p=SafeExecutionGraphPolicy(LearnedExecutionGraphPolicy(default_path_templates()))
    out=p.route(RoutingContext(risk=.95))
    row=next(x for x in out["ranking"] if x["path"]==out["selected"])
    assert "reasoning" in row["stages"]
