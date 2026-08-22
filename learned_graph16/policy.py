
from learned_graph16.bucket import graph_topology_bucket
from learned_graph16.learner import ExecutionGraphPolicyLearner

class LearnedExecutionGraphPolicy:
    def __init__(self,templates,learner=None):
        self.templates={x.name:x for x in templates}
        self.learner=learner or ExecutionGraphPolicyLearner()

    def route(self,ctx):
        bucket=graph_topology_bucket(ctx)
        ranked=[]
        for p in self.templates.values():
            if ctx.risk<p.risk_floor:continue
            u=self.learner.utility(bucket,p)
            ranked.append({"path":p.name,"utility":u,"stages":p.stages,"observations":self.learner.stats[(bucket,p.name)]["n"]})
        ranked.sort(key=lambda x:x["utility"],reverse=True)
        if not ranked:raise ValueError("no_execution_path")
        return {"selected":ranked[0]["path"],"bucket":bucket,"ranking":ranked}

    def feedback(self,outcome):
        self.learner.observe(outcome)
