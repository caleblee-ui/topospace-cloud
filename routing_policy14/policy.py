
from routing_policy14.features import topology_bucket
from routing_policy14.learner import RoutingPolicyLearner
class LearnedModelRoutingPolicy:
    def __init__(self,profiles,learner=None):
        self.profiles={p.name:p for p in profiles};self.learner=learner or RoutingPolicyLearner()
    def route(self,ctx):
        b=topology_bucket(ctx);ranked=[]
        for p in self.profiles.values():
            if ctx.expected_input_tokens<=p.max_context:
                ranked.append({"model":p.name,"utility":self.learner.utility(b,p),
                               "observations":self.learner.stats[(b,p.name)]["n"]})
        ranked.sort(key=lambda x:x["utility"],reverse=True)
        if not ranked:raise ValueError("no_model_fits_context")
        return {"selected":ranked[0]["model"],"bucket":b,"ranking":ranked}
    def feedback(self,o):self.learner.observe(o)
