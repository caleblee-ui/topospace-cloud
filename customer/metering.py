
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass,asdict
import threading,time,json

@dataclass
class UsageEvent:
    tenant_id:str
    metric:str
    quantity:float
    ts:float
    metadata:dict

class UsageMeter:
    def __init__(self):
        self.events=[];self.totals=defaultdict(float);self.lock=threading.RLock()

    def record(self,tenant_id,metric,quantity=1,metadata=None):
        e=UsageEvent(tenant_id,metric,float(quantity),time.time(),metadata or {})
        with self.lock:
            self.events.append(e)
            self.totals[(tenant_id,metric)]+=float(quantity)
        return e

    def total(self,tenant_id,metric):
        with self.lock:return self.totals[(tenant_id,metric)]

    def snapshot(self,tenant_id=None):
        with self.lock:
            rows=[asdict(x) for x in self.events if tenant_id is None or x.tenant_id==tenant_id]
        return rows
