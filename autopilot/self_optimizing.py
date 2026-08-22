
from __future__ import annotations
from autopilot.runtime import AutopilotRuntime
from autopilot.models import RuntimeSignals
from learning_runtime.bandit import ContextualBandit
from learning_runtime.optimizer import BayesianStyleOptimizer
from learning_runtime.objective import ConstrainedEfficiencyObjective

class SelfOptimizingAutopilot:
    """Learns operating profiles while retaining the deterministic safety controller."""
    PROFILES={
      "conservative":{"epsilon_scale":1.15,"token_scale":1.20,"memory_scale":1.15},
      "balanced":{"epsilon_scale":1.00,"token_scale":1.00,"memory_scale":1.00},
      "efficient":{"epsilon_scale":.82,"token_scale":.72,"memory_scale":.80},
    }

    def __init__(self):
        self.base=AutopilotRuntime()
        self.bandit=ContextualBandit(self.PROFILES.keys())
        self.search=BayesianStyleOptimizer()
        self.objective=ConstrainedEfficiencyObjective()

    def decide(self,signals:RuntimeSignals):
        base=self.base.update(signals)
        ctx={"uncertainty":signals.uncertainty,"complexity":base["decision"]["exploration"],
             "cost_pressure":signals.token_pressure}
        profile=self.bandit.select(ctx)
        d=dict(base["decision"]);p=self.PROFILES[profile]
        d["epsilon"]=max(.16,min(.68,d["epsilon"]*p["epsilon_scale"]))
        d["max_context_tokens"]=max(6000,min(48000,round(d["max_context_tokens"]*p["token_scale"])))
        d["memory_recall_limit"]=max(4,min(30,round(d["memory_recall_limit"]*p["memory_scale"])))
        d["profile"]=profile
        return {"signals":signals.__dict__.copy(),"decision":d,"context_bucket":self.bandit.bucket(ctx)}

    def learn(self,decision,*,success_rate,token_reduction,cost_reduction,latency_norm,risk=0.0):
        score=self.objective.evaluate(success_rate=success_rate,token_reduction=token_reduction,
                                      cost_reduction=cost_reduction,latency_norm=latency_norm,risk=risk)
        ctx={"uncertainty":decision["signals"]["uncertainty"],
             "complexity":decision["decision"]["exploration"],
             "cost_pressure":decision["signals"]["token_pressure"]}
        profile=decision["decision"]["profile"]
        self.bandit.update(ctx,profile,score["reward"],score["feasible"])
        self.search.observe({
          "epsilon":decision["decision"]["epsilon"],
          "p":decision["decision"]["p"],
          "tokens":decision["decision"]["max_context_tokens"],
        },score["reward"],score["feasible"])
        return score
