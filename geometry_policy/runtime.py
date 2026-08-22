
from geometry_policy.model import PolicyState
from geometry_policy.network import GeometryPolicyNetwork
from geometry_policy.controller import AdaptiveGeometryController

class LearnedGeometryRuntime:
    def __init__(self,n_views=7):
        self.policy=GeometryPolicyNetwork(n_views=n_views)
        self.controller=AdaptiveGeometryController(self.policy)

    def query(self,candidates,**state):
        s=PolicyState(**state)
        return self.controller.retrieve(s,candidates)
