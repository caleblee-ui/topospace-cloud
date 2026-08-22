
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Dict, Any, List
from runtime.decision_runtime import TopoDecisionRuntime, Candidate
from runtime.context_budget import ContextBudgetManager

@dataclass
class AgentStepResult:
    step:int
    objective:str
    selected:dict
    action:dict
    success:bool

class TopologicalAgentRuntime:
    """Reference agent loop where TopoSpace controls visible context."""

    def __init__(self, decision=None, budget=None):
        self.decision=decision or TopoDecisionRuntime()
        self.budget=budget or ContextBudgetManager()
        self.trace=[]

    def step(self, objective, candidates, weighted_edges, executor: Callable[[dict],dict], step_no=0):
        budgets=self.budget.budgets(objective)
        selected={}
        for typ,limit in budgets.items():
            d=self.decision.select(candidates,weighted_edges,limit,[typ])
            selected[typ]=d.selected

        action_payload={"objective":objective,"context":selected}
        outcome=executor(action_payload)
        row=AgentStepResult(step_no,objective,selected,outcome,bool(outcome.get("success")))
        self.trace.append(row)
        return row
