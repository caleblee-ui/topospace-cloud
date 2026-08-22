
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class BudgetPolicy:
    max_items: int = 12
    memory: int = 4
    tool: int = 3
    skill: int = 2
    agent: int = 2
    code: int = 6

class ContextBudgetManager:
    def __init__(self, policy: BudgetPolicy|None=None):
        self.policy=policy or BudgetPolicy()

    def budgets(self, objective: str = ""):
        p=self.policy
        out={"memory":p.memory,"tool":p.tool,"skill":p.skill,"agent":p.agent,"code":p.code}
        low=(objective or "").lower()
        if any(x in low for x in ("debug","bug","fix","test")):
            out["code"]+=2; out["tool"]+=1
        if any(x in low for x in ("research","explain","analyze")):
            out["memory"]+=2
        return out
