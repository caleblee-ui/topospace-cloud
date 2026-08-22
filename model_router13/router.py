
from model_router13.history import ModelOutcomeHistory
from model_router13.scorer import TopologyAwareModelScorer

class TopologyAwareModelRouter:
    def __init__(self,profiles):
        self.profiles={p.name:p for p in profiles}
        self.history=ModelOutcomeHistory()
        self.scorer=TopologyAwareModelScorer(self.history)

    def route(self,ctx):
        ranked=[]
        for p in self.profiles.values():
            if ctx.expected_input_tokens>p.max_context:
                continue
            ranked.append({"model":p.name,"score":self.scorer.score(p,ctx)})
        ranked.sort(key=lambda x:x["score"],reverse=True)
        if not ranked:
            raise ValueError("no_model_fits_context")
        return {"selected":ranked[0]["model"],"ranking":ranked}

    def feedback(self,model,reward,success,latency_ms):
        self.history.record(model,reward,success,latency_ms)
