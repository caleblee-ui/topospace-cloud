
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, List, Dict, Any
from learning.topology_learner import TopologyLearner, TopologyParams

@dataclass
class StepTrace:
    step: int
    params: dict
    outcome: dict
    reward: float

class ReplanningLoop:
    """Retries a task with topology adaptation after failures."""
    def __init__(self, learner: TopologyLearner, max_steps: int = 4):
        self.learner=learner
        self.max_steps=max_steps
        self.trace: List[StepTrace]=[]

    def run(self, attempt: Callable[[TopologyParams,int], Dict[str,Any]]):
        best=None
        for step in range(self.max_steps):
            params = self.learner.params if step==0 else self.learner.propose()
            outcome = attempt(params, step)
            reward = float(outcome.get("reward", 1.0 if outcome.get("success") else -0.5))
            self.learner.update(params, reward)
            self.trace.append(StepTrace(step, {
                "p": params.p, "epsilon": params.epsilon, "weights": dict(params.weights)
            }, outcome, reward))
            if best is None or reward > best["reward"]:
                best={"reward":reward,"outcome":outcome,"params":params}
            if outcome.get("success"):
                break
        return {"best": best, "trace": [asdict(x) for x in self.trace]}
