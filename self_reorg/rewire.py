
class TopologyRewirer:
    """Activates strong paths, deactivates weak ones, and creates useful shortcuts."""
    def __init__(self,prune_threshold=.15,shortcut_threshold=.82):
        self.prune_threshold=prune_threshold
        self.shortcut_threshold=shortcut_threshold

    def prune(self,graph):
        changed=0
        for e in graph.edges:
            if e.weight<self.prune_threshold and e.active:
                e.active=False;changed+=1
        return changed

    def reactivate(self,graph):
        changed=0
        for e in graph.edges:
            if e.weight>=self.prune_threshold and not e.active:
                e.active=True;changed+=1
        return changed

    def create_shortcuts(self,graph,task_id):
        existing={(e.source,e.target) for e in graph.edges}|{(e.target,e.source) for e in graph.edges}
        added=0
        if task_id not in graph.nodes:return 0
        strong=[n for n in graph.nodes.values() if n.id!=task_id and n.score>=self.shortcut_threshold and n.state=="available"]
        for n in strong:
            if (task_id,n.id) not in existing:
                graph.connect(task_id,n.id,"learned_shortcut",min(1.0,n.score))
                existing.add((task_id,n.id));added+=1
        return added
