
from general_geometry.engine import GeneralizedGeometryEngine
from geometry_policy.compiler import GeometryCompiler

class AdaptiveGeometryController:
    def __init__(self,policy,compiler=None):
        self.policy=policy
        self.compiler=compiler or GeometryCompiler()

    def build_engine(self,state):
        decision=self.policy.decide(state)
        agg=self.compiler.compile(decision)
        return decision,GeneralizedGeometryEngine(agg)

    def retrieve(self,state,candidates):
        decision,engine=self.build_engine(state)
        selected=engine.neighborhood(candidates,decision.epsilon)
        return {"decision":decision,"selected":selected}

    def feedback(self,state,decision,reward):
        self.policy.update(state,decision,reward)
