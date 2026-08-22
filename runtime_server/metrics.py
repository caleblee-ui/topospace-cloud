
from collections import defaultdict
import time
class RuntimeMetrics:
    def __init__(self):
        self.counters=defaultdict(int);self.latencies=defaultdict(list)
    def record(self,hook,ms,ok=True):
        self.counters[(hook,"ok" if ok else "error")]+=1
        self.latencies[hook].append(float(ms))
    def snapshot(self):
        out={}
        for hook,xs in self.latencies.items():
            ys=sorted(xs)
            out[hook]={"count":len(xs),"p95_ms":ys[max(0,int(.95*len(ys))-1)] if ys else 0}
        return out
