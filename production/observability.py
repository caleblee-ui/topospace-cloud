
from __future__ import annotations
from collections import defaultdict,deque
from contextlib import contextmanager
from time import perf_counter,time
import threading

class Observability:
    def __init__(self,max_events=5000):
        self.counters=defaultdict(int);self.timings=defaultdict(list);self.events=deque(maxlen=max_events);self.lock=threading.RLock()

    def count(self,name,value=1):
        with self.lock:self.counters[name]+=value

    def event(self,name,**payload):
        with self.lock:self.events.append({"ts":time(),"event":name,**payload})

    @contextmanager
    def timer(self,name):
        s=perf_counter()
        try:yield
        finally:
            with self.lock:self.timings[name].append((perf_counter()-s)*1000)

    def snapshot(self):
        with self.lock:
            return {"counters":dict(self.counters),
                    "timings":{k:{"count":len(v),"mean_ms":sum(v)/len(v) if v else 0,"p95_ms":sorted(v)[max(0,int(.95*len(v))-1)] if v else 0} for k,v in self.timings.items()},
                    "recent_events":list(self.events)[-100:]}
