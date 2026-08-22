
from learning.topology_learner import TopologyLearner
from learning.multi_objective import MultiObjectiveTopologyLearner
from topology.drift import TopologicalDrift
from topology.persistence import zero_dim_persistence
from runtime.persistent_context import PersistentContextSelector
from runtime.drift_replanner import DriftAwareReplanner

def test_multiobjective_reward():
    l=MultiObjectiveTopologyLearner(TopologyLearner(seed=3))
    good=l.reward({"success":1,"token_cost_norm":.1,"latency_norm":.1,"tool_calls_norm":.1,"risk":.1})
    bad=l.reward({"success":0,"token_cost_norm":1,"latency_norm":1,"tool_calls_norm":1,"risk":1})
    assert good > bad

def test_drift():
    a={"nodes":["a","b"],"edges":[("a","b")]}
    b={"nodes":["a","c","d"],"edges":[("a","c")]}
    report=TopologicalDrift().compare(a,b)
    assert report.score > 0 and "c" in report.entered and "b" in report.exited

def test_persistence():
    ints=zero_dim_persistence(["a","b","c"],[("a","b",.1),("b","c",.5)])
    finite=[x for x in ints if x.death is not None]
    infinite=[x for x in ints if x.death is None]
    assert len(finite)==2 and len(infinite)==1
    assert max(x.persistence for x in finite)==.5

def test_persistent_context_rank():
    r=PersistentContextSelector().rank(["a","b","c"],[("a","b",.1),("b","c",.6)])
    assert r[0][1] >= r[-1][1]

def test_drift_replanner():
    d=DriftAwareReplanner(threshold=.2)
    yes,report=d.should_replan({"nodes":["a"],"edges":[]},{"nodes":["b"],"edges":[]})
    assert yes
