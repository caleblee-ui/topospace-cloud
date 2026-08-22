
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class TokenBudget:
    max_input_tokens:int=32000
    reserve_output_tokens:int=4000
    min_success_margin:float=.02

class TokenBudgetController:
    """Budget context before prompt construction; token counts are supplied by adapters."""
    def __init__(self,budget=None):
        self.budget=budget or TokenBudget()

    def prune(self,items:List[dict]):
        cap=max(0,self.budget.max_input_tokens-self.budget.reserve_output_tokens)
        ranked=sorted(items,key=lambda x:(x.get("utility",0)/max(1,x.get("tokens",1))),reverse=True)
        kept=[]; used=0
        for x in ranked:
            t=int(x.get("tokens",0))
            if used+t<=cap:
                kept.append(x);used+=t
        return {"kept":kept,"dropped":[x for x in items if x not in kept],"tokens":used,"capacity":cap}
