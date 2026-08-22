
from dynamic_topology.runtime import DynamicTopologyRuntime
from optimization_v2.adaptive_metric import DynamicPNorm,AdaptiveEpsilon
from self_reorg.learner import TopologyReinforcementLearner
from self_reorg.rewire import TopologyRewirer
from self_reorg.memory_growth import TorusMemoryTopologyAdapter

class SelfReorganizingTopologyRuntime:
    def __init__(self):
        self.runtime=DynamicTopologyRuntime()
        self.metric=DynamicPNorm()
        self.epsilon_selector=AdaptiveEpsilon()
        self.learner=TopologyReinforcementLearner()
        self.rewirer=TopologyRewirer()
        self.memory=TorusMemoryTopologyAdapter()
        self.step=0

    @property
    def graph(self): return self.runtime.graph

    def add(self,*args,**kwargs): return self.runtime.add(*args,**kwargs)
    def link(self,*args,**kwargs): return self.runtime.link(*args,**kwargs)

    def adaptive_geometry(self,task_id):
        neighbors=[n for n,e in self.graph.neighbors(task_id)]
        if not neighbors:return {"p":2.0,"epsilon":.1}
        vectors=[[n.score,1-n.distance,float(n.metadata.get("importance",.5))] for n in neighbors]
        p=self.metric.choose_p(vectors)
        epsilon=self.epsilon_selector.choose([n.distance for n in neighbors])
        return {"p":p,"epsilon":epsilon}

    def ingest_memories(self,task_id,memories):
        return self.memory.ingest(self.graph,task_id,memories)

    def execute(self,task_id,max_steps=8):
        self.step+=1
        geo=self.adaptive_geometry(task_id)
        plan=self.runtime.execute_plan(task_id,max_steps)
        return {"step":self.step,"geometry":geo,**plan}

    def feedback(self,task_id,executed_steps,outcomes):
        """outcomes: {node_id: {"success":bool,"reward":0..1}}"""
        strengthened=[];weakened=[]
        for step in executed_steps:
            nid=step["to"];out=outcomes.get(nid,{"success":False,"reward":0})
            node=self.graph.nodes[nid]
            old=node.score;new=self.learner.update_node(node,out["reward"],out["success"])
            (strengthened if new>=old else weakened).append(nid)
            for e in self.graph.edges:
                if ((e.source==step["from"] and e.target==nid) or (e.target==step["from"] and e.source==nid)) and e.relation==step["relation"]:
                    self.learner.update_edge(e,out["reward"],out["success"])
                    break
        pruned=self.rewirer.prune(self.graph)
        reactivated=self.rewirer.reactivate(self.graph)
        shortcuts=self.rewirer.create_shortcuts(self.graph,task_id)
        self.graph.version+=1
        return {
          "graph_version":self.graph.version,
          "strengthened":strengthened,
          "weakened":weakened,
          "pruned_edges":pruned,
          "reactivated_edges":reactivated,
          "shortcuts_added":shortcuts
        }
