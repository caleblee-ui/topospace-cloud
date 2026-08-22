
from unified_runtime.models import AgentState
from unified_runtime.runtime import UnifiedAdaptiveAgentRuntime
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder
from unified_runtime.lifecycle import UnifiedRuntimeLifecycle

def sample(kind,n=8):
    xs=[]
    for i in range(n):
        xs.append({
          "id":f"{kind}-{i}","kind":kind,
          "semantic_distance":.08 if i<3 else .7,
          "structural_distance":.10 if i<3 else .65,
          "history_distance":.12 if i<3 else .6,
          "policy_distance":0 if i<3 else (1.0 if kind in {"tool","plan"} else 0),
          "security_distance":0 if i<3 else (1.0 if kind=="tool" else 0),
          "cost_distance":.1 if i<3 else .5,
          "reliability_distance":.1 if i<3 else .6,
        })
    return xs

def test_all_domains_route():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder()
    s=AgentState("t","x",risk=.7,hierarchy=.7)
    spaces={d:b.build_space(sample(d)) for d in ("memory","tool","skill","plan")}
    out=r.build_execution_space(s,spaces)
    assert set(out["routes"])=={"memory","tool","skill","plan"}

def test_tool_hard_constraints_blocked():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder()
    s=AgentState("t","x",risk=.2)
    out=r.build_execution_space(s,{"memory":[],"tool":b.build_space(sample("tool")),"skill":[],"plan":[]})
    selected=[x["id"] for x in out["routes"]["tool"]["selected"]]
    assert all(x in {"tool-0","tool-1","tool-2"} for x in selected)
    assert len(out["routes"]["tool"]["blocked_by_constraints"])==5

def test_security_tool_geometry_noncompensatory():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder()
    s=AgentState("t","x",risk=1.0)
    out=r.build_execution_space(s,{"memory":[],"tool":b.build_space(sample("tool")),"skill":[],"plan":[]})
    assert out["geometry"]["tool"]["aggregator"] in {"chebyshev","nested"}

def test_planning_prefers_nested_under_hierarchy():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder()
    s=AgentState("t","x",hierarchy=1.0)
    out=r.build_execution_space(s,{"memory":[],"tool":[],"skill":[],"plan":b.build_space(sample("plan"))})
    assert out["geometry"]["plan"]["aggregator"]=="nested"

def test_learning_feedback():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder()
    s=AgentState("t","x",ambiguity=.8)
    out=r.build_execution_space(s,{d:b.build_space(sample(d)) for d in ("memory","tool","skill","plan")})
    rewards=r.learn(out,{"memory":{"relevant_selected":2,"total_relevant":3,"token_cost":500}})
    assert "memory" in rewards

def test_lifecycle_bridge():
    r=UnifiedAdaptiveAgentRuntime();b=RuntimeSpaceBuilder();lc=UnifiedRuntimeLifecycle(r,b)
    s=AgentState("t","x")
    out=lc.prepare(s,{"memory":sample("memory"),"tool":[],"skill":[],"plan":[]})
    assert "bundle" in out
