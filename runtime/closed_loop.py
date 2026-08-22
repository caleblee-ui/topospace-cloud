
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, Dict, Any, List
from runtime.decision_runtime import TopoDecisionRuntime, Candidate
from runtime.context_budget import ContextBudgetManager
from topology.drift import TopologicalDrift
from learning.topology_learner import TopologyLearner, TopologyParams
from learning.multi_objective import MultiObjectiveTopologyLearner

@dataclass
class LoopStep:
    step: int
    objective: str
    selected: Dict[str, list]
    observation: Dict[str, Any]
    drift_score: float
    reward: float
    topology: Dict[str, Any]
    replanned: bool

class ClosedLoopTopoAgent:
    """Closed-loop runtime:
    state -> topology -> context -> action -> observation -> drift -> reward -> learning -> replan
    """
    def __init__(self, decision=None, budget=None, learner=None, drift_threshold=.30, max_steps=6):
        self.decision=decision or TopoDecisionRuntime()
        self.budget=budget or ContextBudgetManager()
        self.base_learner=learner or TopologyLearner(seed=17)
        self.multi=MultiObjectiveTopologyLearner(self.base_learner)
        self.drift=TopologicalDrift()
        self.drift_threshold=drift_threshold
        self.max_steps=max_steps
        self.trace: List[LoopStep]=[]

    def _snapshot(self, candidates, edges):
        return {
          "nodes":[c.id for c in candidates],
          "edges":[(a,b) for a,b,*_ in edges]
        }

    def run(self, objective: str, candidates: List[Candidate], weighted_edges,
            executor: Callable[[dict,int], Dict[str,Any]],
            mutate: Callable[[List[Candidate],list,Dict[str,Any],int], tuple]|None=None):
        current_candidates=list(candidates)
        current_edges=list(weighted_edges)
        previous=self._snapshot(current_candidates,current_edges)

        for step in range(self.max_steps):
            budgets=self.budget.budgets(objective)
            selected={}
            for typ,limit in budgets.items():
                selected[typ]=self.decision.select(
                    current_candidates,current_edges,limit,[typ]
                ).selected

            payload={
              "objective":objective,
              "context":selected,
              "topology":{
                "p":self.base_learner.params.p,
                "epsilon":self.base_learner.params.epsilon,
                "weights":dict(self.base_learner.params.weights)
              }
            }
            obs=executor(payload,step)

            metrics={
              "success":1.0 if obs.get("success") else 0.0,
              "token_cost_norm":obs.get("token_cost_norm",0.0),
              "latency_norm":obs.get("latency_norm",0.0),
              "tool_calls_norm":obs.get("tool_calls_norm",0.0),
              "risk":obs.get("risk",0.0)
            }
            candidate_params=self.base_learner.propose()
            _,reward=self.multi.update(candidate_params,metrics)

            if mutate:
                current_candidates,current_edges=mutate(
                    current_candidates,current_edges,obs,step
                )

            current=self._snapshot(current_candidates,current_edges)
            report=self.drift.compare(previous,current)
            replan=(not obs.get("success")) or report.score>=self.drift_threshold

            self.trace.append(LoopStep(
                step,objective,selected,obs,report.score,reward,
                {"p":self.base_learner.params.p,
                 "epsilon":self.base_learner.params.epsilon,
                 "weights":dict(self.base_learner.params.weights)},
                replan
            ))

            if obs.get("success"):
                break
            previous=current

        return {
          "success":bool(self.trace and self.trace[-1].observation.get("success")),
          "steps":[asdict(x) for x in self.trace],
          "final_topology":{
             "p":self.base_learner.params.p,
             "epsilon":self.base_learner.params.epsilon,
             "weights":dict(self.base_learner.params.weights)
          }
        }
