
from __future__ import annotations
import hashlib,json,time

class TopologyCache:
    def __init__(self,ttl_seconds=300):
        self.ttl=ttl_seconds;self.data={}

    def key(self,objective,items,p,epsilon):
        stable=[(x.get("id"),x.get("distance"),x.get("score"),x.get("tokens")) for x in items]
        raw=json.dumps([objective,stable,p,epsilon],sort_keys=True,separators=(",",":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def get(self,key):
        row=self.data.get(key)
        if not row:return None
        if time.time()-row["ts"]>self.ttl:
            self.data.pop(key,None);return None
        return row["value"]

    def set(self,key,value):
        self.data[key]={"ts":time.time(),"value":value}
        return value
