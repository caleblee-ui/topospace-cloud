
from optimization_v2.hybrid_router import HybridTopologyRouter

class CoarseToFineRecall:
    """Search nearest topology shells first, widening only when budget/quality requires it."""
    def __init__(self,router=None):
        self.router=router or HybridTopologyRouter()

    def select(self,hierarchy,token_budget=4000,min_items=2,min_score=.35):
        selected=[];used=0;visited=[]
        for level in sorted(hierarchy):
            visited.append(level)
            for n in self.router.rank([{
                "id":x.id,"distance":x.distance,"utility":x.utility,"tokens":x.tokens,
                "score":(x.payload or {}).get("score",x.utility),
                "drift":(x.payload or {}).get("drift",0),"node":x
            } for x in hierarchy[level]]):
                node=n["node"]
                if self.router.score(n)<min_score and len(selected)>=min_items:continue
                if used+node.tokens>token_budget and selected:continue
                selected.append(node);used+=node.tokens
            if len(selected)>=min_items and used>=token_budget*.45:
                break
        return {"nodes":selected,"tokens":used,"visited_levels":visited}
