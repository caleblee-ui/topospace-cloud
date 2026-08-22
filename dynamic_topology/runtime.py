
from dynamic_topology.graph import DynamicAgentTopology,RuntimeNode
from dynamic_topology.planner import TopologicalExecutionPlanner

class DynamicTopologyRuntime:
    def __init__(self):
        self.graph=DynamicAgentTopology();self.planner=TopologicalExecutionPlanner();self.events=[]

    def add(self,id,kind,**kwargs):
        n=self.graph.upsert_node(RuntimeNode(id=id,kind=kind,**kwargs))
        self.events.append({"type":"node_upsert","id":id,"version":self.graph.version});return n

    def link(self,a,b,relation,weight=1):
        e=self.graph.connect(a,b,relation,weight)
        self.events.append({"type":"edge_add","source":a,"target":b,"relation":relation,"version":self.graph.version});return e

    def execute_plan(self,task_id,max_steps=8):
        plan=self.planner.plan(self.graph,task_id,max_steps)
        self.events.append({"type":"plan","task":task_id,"steps":len(plan),"version":self.graph.version})
        return {"graph_version":self.graph.version,"plan":plan,"snapshot":self.graph.snapshot()}

    def update_outcome(self,node_id,success,reward):
        n=self.graph.nodes[node_id]
        n.score=max(0,min(1,.8*n.score+.2*(float(reward) if success else 0)))
        n.state="available";self.graph.version+=1
        self.events.append({"type":"outcome","id":node_id,"success":bool(success),"reward":float(reward),"version":self.graph.version})
