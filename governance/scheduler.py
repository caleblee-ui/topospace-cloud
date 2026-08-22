
from __future__ import annotations
import time,heapq

class RolloutScheduler:
    def __init__(self):
        self.q=[]

    def schedule(self,when_ts,tenant_id,task_type,version,percent=100):
        item=(float(when_ts),{"tenant_id":tenant_id,"task_type":task_type,"version":int(version),"percent":int(percent)})
        heapq.heappush(self.q,item);return item[1]

    def due(self,now=None):
        now=time.time() if now is None else float(now)
        out=[]
        while self.q and self.q[0][0]<=now:
            out.append(heapq.heappop(self.q)[1])
        return out
