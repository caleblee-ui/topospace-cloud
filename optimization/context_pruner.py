
class TopologicalContextPruner:
    def prune(self,items,epsilon=.35,min_score=.25,max_drift=.45):
        kept=[]; dropped=[]
        for x in items:
            distance=float(x.get("distance",1))
            score=float(x.get("score",0))
            drift=float(x.get("drift",0))
            (kept if distance<=epsilon and score>=min_score and drift<=max_drift else dropped).append(x)
        return {"kept":kept,"dropped":dropped}
