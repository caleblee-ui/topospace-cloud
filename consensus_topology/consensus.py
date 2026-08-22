
class TopologicalConsensus:
    """Aggregates independent agent proposals without requiring identical local graphs."""
    def __init__(self,diversity_weight=.12):
        self.diversity_weight=diversity_weight

    def aggregate(self,proposals):
        groups={}
        for p in proposals: groups.setdefault(p.candidate_id,[]).append(p)
        ranked=[]
        for cid,ps in groups.items():
            agents={p.agent_id for p in ps}
            confidence=sum(p.confidence for p in ps)/len(ps)
            utility=sum(p.utility for p in ps)/len(ps)
            proximity=sum(1-max(0,min(1,p.distance)) for p in ps)/len(ps)
            evidence=sum(p.evidence for p in ps)/len(ps)
            diversity=min(1,len(agents)/max(1,len({p.agent_id for p in proposals})))
            score=.30*confidence+.25*utility+.20*proximity+.13*evidence+self.diversity_weight*diversity
            ranked.append({"candidate_id":cid,"score":score,"support":len(agents),"agents":sorted(agents),"kind":ps[0].kind})
        return sorted(ranked,key=lambda x:(x["score"],x["support"]),reverse=True)
