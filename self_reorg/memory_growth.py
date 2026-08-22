
from dynamic_topology.graph import RuntimeNode

class TorusMemoryTopologyAdapter:
    """Promotes recalled TorusDB memories into runtime topology nodes."""
    def ingest(self,graph,task_id,memories):
        added=[]
        for m in memories:
            mid=m.get("id")
            if not mid:continue
            if mid not in graph.nodes:
                graph.upsert_node(RuntimeNode(
                    id=mid,kind="memory",
                    score=float(m.get("score",m.get("utility",m.get("importance",.5)))),
                    distance=float(m.get("distance",1)),
                    metadata={"torusdb":True,**dict(m.get("metadata",{}))}
                ))
                added.append(mid)
            if not any((e.source==task_id and e.target==mid) or (e.target==task_id and e.source==mid) for e in graph.edges):
                graph.connect(task_id,mid,"recall",float(m.get("score",m.get("utility",.5))))
        return added
