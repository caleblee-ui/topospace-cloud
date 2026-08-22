
from performance.delta import TopologyDelta,DeltaApplier
from performance.incremental_neighborhood import IncrementalNeighborhood
from indexing.sharded import ShardedObjectIndex

class TopologyDeltaRuntime:
    def __init__(self,epsilon=.35,shards=16):
        self.nodes={}
        self.edges=set()
        self.applier=DeltaApplier()
        self.neighborhood=IncrementalNeighborhood(epsilon=epsilon)
        self.index=ShardedObjectIndex(shards)

    def bootstrap(self,nodes,edges):
        self.nodes={n["id"]:dict(n) for n in nodes};self.edges=set(tuple(e) for e in edges)
        for k,v in self.nodes.items():self.index.put(k,v)
        self.neighborhood.rebuild(nodes)

    def apply(self,delta:TopologyDelta):
        self.nodes,self.edges=self.applier.apply(self.nodes,self.edges,delta)
        for nid in delta.removed_node_ids:self.index.delete(nid)
        for obj in delta.added_nodes+delta.updated_nodes:self.index.put(obj["id"],obj)
        members=self.neighborhood.apply_delta(delta.added_nodes,delta.updated_nodes,delta.removed_node_ids)
        return {"nodes":len(self.nodes),"edges":len(self.edges),"neighborhood":members}
