
from __future__ import annotations
from collections import deque
from threading import RLock
from time import time

class OperationsStore:
    def __init__(self,max_events=2000):
        self.events=deque(maxlen=max_events);self.lock=RLock()

    def record(self,event_type,tenant_id="default",**payload):
        with self.lock:
            e={"ts":time(),"type":event_type,"tenant_id":tenant_id,**payload}
            self.events.append(e);return e

    def recent(self,tenant_id=None,limit=100):
        with self.lock:
            rows=list(self.events)
        if tenant_id: rows=[x for x in rows if x["tenant_id"]==tenant_id]
        return rows[-limit:]

    def topology(self,tenant_id=None):
        rows=self.recent(tenant_id,500)
        nodes={};edges=[]
        for e in rows:
            if e["type"]=="optimization":
                task=e.get("request_id","task")
                nodes[task]={"id":task,"kind":"task","label":e.get("objective","task")}
                for x in e.get("selected_context",[]):
                    nid=x.get("id","context")
                    nodes[nid]={"id":nid,"kind":x.get("type","context"),"label":nid,
                                "score":x.get("score",x.get("utility",.5)),
                                "distance":x.get("distance",.5)}
                    edges.append({"source":task,"target":nid,"weight":x.get("score",x.get("utility",.5))})
        return {"nodes":list(nodes.values()),"edges":edges}
