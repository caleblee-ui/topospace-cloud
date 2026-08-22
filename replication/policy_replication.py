
from __future__ import annotations
import threading,hashlib,json

class MultiRegionPolicyReplicator:
    def __init__(self,regions):
        self.regions={r:{} for r in regions};self.lock=threading.RLock()

    @staticmethod
    def digest(payload):
        return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(",",":")).encode()).hexdigest()

    def replicate(self,key,payload):
        d=self.digest(payload)
        with self.lock:
            for region in self.regions:
                self.regions[region][key]={"payload":payload,"hash":d}
        return {"regions":list(self.regions),"hash":d}

    def verify(self,key):
        with self.lock:
            rows=[v.get(key) for v in self.regions.values()]
        if any(x is None for x in rows):return False
        return len({x["hash"] for x in rows})==1
