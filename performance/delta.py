
from dataclasses import dataclass, field
from typing import Dict, Any, List, Tuple

@dataclass
class TopologyDelta:
    added_nodes:List[dict]=field(default_factory=list)
    removed_node_ids:List[str]=field(default_factory=list)
    updated_nodes:List[dict]=field(default_factory=list)
    added_edges:List[tuple]=field(default_factory=list)
    removed_edges:List[tuple]=field(default_factory=list)

class DeltaApplier:
    def apply(self,nodes:Dict[str,dict],edges:set,delta:TopologyDelta):
        for nid in delta.removed_node_ids:
            nodes.pop(nid,None)
            edges={e for e in edges if nid not in e[:2]}
        for n in delta.added_nodes:
            nodes[n["id"]]=dict(n)
        for n in delta.updated_nodes:
            nodes.setdefault(n["id"],{}).update(n)
        for e in delta.removed_edges:
            edges.discard(tuple(e))
        for e in delta.added_edges:
            edges.add(tuple(e))
        return nodes,edges
