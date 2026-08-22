
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder
from unified_runtime.router import UnifiedAdaptiveRouter
from coupled_geometry.runtime import CrossDomainGeometryRuntime
from coupled_geometry.coupling import CrossDomainCoupling
from joint_optimizer.controller import JointGeometryController
from joint_optimizer.objective import JointUtility
from joint_optimizer.models import JointObjective

class JointGeometryRuntime:
    def __init__(self):
        self.controller=JointGeometryController()
        self.utility=JointUtility()

    def solve(self,agent_state,spaces):
        decision=self.controller.decide(agent_state)
        runtime=CrossDomainGeometryRuntime(max_iterations=4)

        # Inject learned local geometry policy and learned coupling field.
        runtime.router.policy=self.controller.geometry
        runtime.coupling=CrossDomainCoupling(decision["field"].couplings)

        solution=runtime.solve(agent_state,spaces)
        solution["joint_decision"]=decision
        return solution

    def feedback(self,solution,rewards_by_domain,task_reward,token_cost=0.0,
                 latency_cost=0.0,violations=0,instability=0.0):
        obj=JointObjective(task_reward,token_cost,latency_cost,violations,instability)
        score=self.utility.score(obj)
        self.controller.update(solution["joint_decision"],rewards_by_domain,score)
        return {"joint_score":score,"objective":obj}
