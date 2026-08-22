
from meta_policy17.controller import MetaPolicyController
from meta_policy17.learner import MetaPolicyLearner
from meta_policy17.objective import MetaUtility
from meta_policy17.models import MetaObjective

class MetaPolicyRuntime:
    def __init__(self):
        self.controller=MetaPolicyController()
        self.learner=MetaPolicyLearner(self.controller)
        self.utility=MetaUtility()
        self.history=[]

    def decide(self,agent_state,routing_ctx):
        d=self.controller.decide(agent_state,routing_ctx)
        self.history.append(d)
        return d

    def feedback(self,decision,routing_ctx,quality,cost,latency,success,violations=0,instability=0):
        obj=MetaObjective(float(quality),float(cost),float(latency),1.0 if success else 0.0,int(violations),float(instability))
        score=self.utility.score(obj)
        self.learner.update(decision,routing_ctx,quality,cost,latency,success,violations,score)
        return {"meta_score":score,"objective":obj}
