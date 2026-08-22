
from dataclasses import dataclass,field
import time

@dataclass
class RuntimeNode:
    id:str
    kind:str
    score:float=.5
    distance:float=1.0
    state:str="available"
    metadata:dict=field(default_factory=dict)
    updated_at:float=field(default_factory=time.time)

@dataclass
class RuntimeEdge:
    source:str
    target:str
    relation:str
    weight:float=1.0
    active:bool=True

class DynamicAgentTopology:
    VALID_KINDS={"task","agent","tool","memory","context"}
    def __init__(self):
        self.nodes={};self.edges=[];self.version=0

    def upsert_node(self,node):
        if node.kind not in self.VALID_KINDS:raise ValueError("invalid_node_kind")
        self.nodes[node.id]=node;self.version+=1;return node

    def connect(self,source,target,relation,weight=1.0):
        if source not in self.nodes or target not in self.nodes:raise KeyError("unknown_node")
        e=RuntimeEdge(source,target,relation,float(weight));self.edges.append(e);self.version+=1;return e

    def neighbors(self,node_id,active_only=True):
        out=[]
        for e in self.edges:
            if active_only and not e.active:continue
            if e.source==node_id:out.append((self.nodes[e.target],e))
            elif e.target==node_id:out.append((self.nodes[e.source],e))
        return out

    def snapshot(self):
        return {"version":self.version,"nodes":[vars(x) for x in self.nodes.values()],"edges":[vars(x) for x in self.edges]}
