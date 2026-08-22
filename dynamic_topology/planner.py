
class TopologicalExecutionPlanner:
    """Ranks reachable runtime nodes by topology, utility and edge affinity."""
    KIND_BONUS={"memory":.05,"context":.04,"tool":.08,"agent":.07,"task":0}
    def rank_neighbors(self,graph,node_id):
        rows=[]
        for node,edge in graph.neighbors(node_id):
            proximity=1-max(0,min(1,node.distance))
            value=.42*node.score+.33*proximity+.20*edge.weight+self.KIND_BONUS.get(node.kind,0)
            if node.state!="available":value-=.5
            rows.append({"node":node,"edge":edge,"value":value})
        return sorted(rows,key=lambda x:x["value"],reverse=True)

    def plan(self,graph,task_id,max_steps=8):
        visited={task_id};frontier=[task_id];steps=[]
        while frontier and len(steps)<max_steps:
            cur=frontier.pop(0)
            for row in self.rank_neighbors(graph,cur):
                n=row["node"]
                if n.id in visited:continue
                visited.add(n.id);frontier.append(n.id)
                steps.append({"from":cur,"to":n.id,"kind":n.kind,"relation":row["edge"].relation,"value":row["value"]})
                if len(steps)>=max_steps:break
        return steps
