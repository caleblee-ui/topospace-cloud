
from optimization.adaptive_controller import AdaptiveOptimizationController
from optimization.quality_guard import QualityPreservationGuard
from production.adaptive_engine import AdaptiveTopoSpaceEngine

def test_controller_expands_with_uncertainty():
 c=AdaptiveOptimizationController()
 low=c.decide(uncertainty=.1,complexity=.2,cost_pressure=.8)
 high=c.decide(uncertainty=.9,complexity=.9,cost_pressure=.1,previous_success=False)
 assert high["epsilon"]>low["epsilon"]
 assert high["max_context_tokens"]>low["max_context_tokens"]

def test_quality_guard():
 q=QualityPreservationGuard()
 assert q.should_expand(uncertainty=.8,previous_success=True,kept_items=5)["expand"]
 assert q.should_expand(uncertainty=.2,previous_success=False,kept_items=5)["expand"]

def test_adaptive_engine_quality_expansion():
 c=[{"id":"a","tokens":100,"utility":1,"distance":.1,"score":.9,"drift":.1},
    {"id":"b","tokens":100,"utility":.8,"distance":.5,"score":.7,"drift":.1}]
 a=[{"id":"agent","capabilities":["code"],"score":.9,"reliability":1,"cost":.1,"risk":.05}]
 r=AdaptiveTopoSpaceEngine().optimize_adaptive("x",c,a,["code"],uncertainty=.9,previous_success=False)
 assert r["expanded_for_quality"] is True
 assert len(r["context"])>=1
