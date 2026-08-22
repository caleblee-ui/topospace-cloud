
class HybridTopologyRouter:
    """Combines semantic relevance, topology distance, utility and drift."""
    def __init__(self,semantic=.42,topology=.33,utility=.20,drift=.05):
        self.w=(semantic,topology,utility,drift)

    def score(self,item):
        semantic=float(item.get("score",item.get("semantic_score",0)))
        distance=max(0.0,min(1.0,float(item.get("distance",1))))
        utility=float(item.get("utility",item.get("importance",.5)))
        drift=max(0.0,min(1.0,float(item.get("drift",0))))
        a,b,c,d=self.w
        return a*semantic+b*(1-distance)+c*utility-d*drift

    def rank(self,items):
        return sorted(items,key=self.score,reverse=True)
