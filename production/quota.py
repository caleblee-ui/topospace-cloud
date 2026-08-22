
from dataclasses import dataclass
from collections import defaultdict
import threading,time

@dataclass
class TenantQuota:
    requests_per_minute:int=120
    max_context_tokens:int=64000
    max_agents:int=8
    max_concurrent:int=16

class QuotaManager:
    def __init__(self):
        self.quotas={};self.windows=defaultdict(list);self.active=defaultdict(int);self.lock=threading.RLock()
    def set_quota(self,tenant_id,quota):self.quotas[tenant_id]=quota
    def get_quota(self,tenant_id):return self.quotas.get(tenant_id,TenantQuota())
    def admit(self,tenant_id):
        now=time.time();q=self.get_quota(tenant_id)
        with self.lock:
            self.windows[tenant_id]=[t for t in self.windows[tenant_id] if now-t<60]
            if len(self.windows[tenant_id])>=q.requests_per_minute:return {"ok":False,"reason":"rate_limit"}
            if self.active[tenant_id]>=q.max_concurrent:return {"ok":False,"reason":"concurrency_limit"}
            self.windows[tenant_id].append(now);self.active[tenant_id]+=1
            return {"ok":True}
    def release(self,tenant_id):
        with self.lock:self.active[tenant_id]=max(0,self.active[tenant_id]-1)
