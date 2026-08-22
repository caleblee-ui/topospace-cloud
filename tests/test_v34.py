
from pathlib import Path
from learning_runtime.bandit import ContextualBandit
from learning_runtime.optimizer import BayesianStyleOptimizer
from learning_runtime.objective import ConstrainedEfficiencyObjective
from autopilot.self_optimizing import SelfOptimizingAutopilot
from autopilot.models import RuntimeSignals

ROOT=Path(__file__).resolve().parents[1]

def test_bandit_updates():
 b=ContextualBandit(["a","b"]);ctx={"uncertainty":.1,"complexity":.1,"cost_pressure":.9}
 a=b.select(ctx);b.update(ctx,a,.5,True)
 assert b._row(b.bucket(ctx),a).pulls==1

def test_optimizer_suggests_in_bounds():
 o=BayesianStyleOptimizer();o.observe({"x":.5},1,True)
 s=o.suggest({"x":(0,1)})
 assert 0<=s["x"]<=1

def test_objective_constraint():
 o=ConstrainedEfficiencyObjective(min_success_rate=.9)
 assert not o.evaluate(success_rate=.8,token_reduction=.5,cost_reduction=.5,latency_norm=.5)["feasible"]

def test_self_optimizing_autopilot():
 a=SelfOptimizingAutopilot();d=a.decide(RuntimeSignals())
 s=a.learn(d,success_rate=.95,token_reduction=.4,cost_reduction=.3,latency_norm=.6)
 assert "profile" in d["decision"] and "reward" in s

def test_learning_visual():
 assert "customElements.define" in (ROOT/"web-sdk/learning-panel.js").read_text()
