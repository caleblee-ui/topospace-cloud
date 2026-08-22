
from execution_graph15.planner import TopologyAwareExecutionGraphPlanner
from execution_graph15.executor import GraphExecutionController
from execution_graph15.policy import EscalationPolicy

class ExecutionGraphRuntime:
    def __init__(self):
        self.planner=TopologyAwareExecutionGraphPlanner()
        self.controller=GraphExecutionController()
        self.policy=EscalationPolicy()

    def plan(self,ctx,model_route,has_tools=False,has_memory=False):
        return self.planner.build(ctx,model_route,has_tools,has_memory)

    def transition(self,graph,current_id,step,signal):
        if self.policy.should_stop(step,signal):
            return {"stop":True,"next":[]}
        return {"stop":False,"next":self.controller.next_nodes(graph,current_id,signal)}
