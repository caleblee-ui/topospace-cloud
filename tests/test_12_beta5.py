
from execution_graph15.planner import TopologyAwareExecutionGraphPlanner
from execution_graph15.executor import GraphExecutionController
from execution_graph15.runtime import ExecutionGraphRuntime
from model_router13.models import RoutingContext

def test_high_complexity_adds_reasoning_escalation():
    g=TopologyAwareExecutionGraphPlanner().build(
      RoutingContext(risk=.8,ambiguity=.8,topology_complexity=.8),
      {"selected":"balanced"},True,True)
    assert any(n.model=="reasoning" for n in g.nodes if n.kind=="model")

def test_low_complexity_graph_small():
    g=TopologyAwareExecutionGraphPlanner().build(RoutingContext(risk=.1,ambiguity=.1,topology_complexity=.1),
                                                  {"selected":"fast"},False,False)
    assert len(g.nodes)==1

def test_failure_triggers_escalation():
    g=TopologyAwareExecutionGraphPlanner().build(RoutingContext(risk=.8),{"selected":"balanced"},False,False)
    nxt=GraphExecutionController().next_nodes(g,"model-primary",{"success":False,"confidence":.2})
    assert "model-reasoning" in nxt

def test_stop_policy():
    r=ExecutionGraphRuntime()
    g=r.plan(RoutingContext(),{"selected":"balanced"})
    out=r.transition(g,"model-primary",1,{"success":True,"confidence":.9,"needs_tool":False})
    assert out["stop"]
