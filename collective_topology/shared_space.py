
from __future__ import annotations
from collective_topology.models import SharedKnowledge

class SharedTopologySpace:
    def __init__(self):
        self.items={}
        self.links=[]

    def publish(self,item:SharedKnowledge):
        self.items[item.id]=item
        return item

    def connect(self,a,b,relation,weight=1.0,tenant_id="default"):
        self.links.append({"source":a,"target":b,"relation":relation,"weight":float(weight),"tenant_id":tenant_id})
        return self.links[-1]

    def visible(self,tenant_id,agent_id=None):
        out=[]
        for x in self.items.values():
            if x.access_scope=="global":
                out.append(x)
            elif x.access_scope=="tenant" and x.tenant_id==tenant_id:
                out.append(x)
            elif x.access_scope=="agent" and x.source_agent==agent_id:
                out.append(x)
        return out
