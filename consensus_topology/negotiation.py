
class ConsensusNegotiator:
    def __init__(self,min_support=2,min_score=.58):
        self.min_support=min_support;self.min_score=min_score
    def decide(self,ranked):
        if not ranked:return {"status":"no_proposal","winner":None}
        top=ranked[0]
        if top["support"]<self.min_support or top["score"]<self.min_score:
            return {"status":"needs_exploration","winner":None,"top":top}
        return {"status":"consensus","winner":top["candidate_id"],"top":top}
