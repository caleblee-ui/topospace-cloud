
from __future__ import annotations
from dataclasses import dataclass, field
from runtime.web_graph_payload import build_graph_payload

@dataclass
class AgentGraphRuntime:
    workspace_id: str
    seq: int = 0
    nodes: dict = field(default_factory=dict)
    edges: dict = field(default_factory=dict)

    def upsert_node(self,node_id,label=None,node_type="context",score=0.0,components=None):
        self.nodes[node_id]={"id":node_id,"label":label or node_id,"type":node_type,"score":float(score),"components":components or {}}
        return self.snapshot()

    def remove_node(self,node_id):
        self.nodes.pop(node_id,None)
        self.edges={k:v for k,v in self.edges.items() if node_id not in k}
        return self.snapshot()

    def connect(self,a,b,distance=.5,edge_type="topological"):
        self.edges[(a,b)]={"source":a,"target":b,"distance":float(distance),"affinity":max(0,1-float(distance)),"type":edge_type}
        return self.snapshot()

    def snapshot(self):
        self.seq+=1
        return {"seq":self.seq,"workspace_id":self.workspace_id,
                "payload":{"state_id":self.workspace_id,"nodes":list(self.nodes.values()),"edges":list(self.edges.values())}}
