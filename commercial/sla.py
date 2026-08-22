from collections import deque
class SLATracker:
    def __init__(self,maxlen=10000): self.latencies=deque(maxlen=maxlen);self.errors=deque(maxlen=maxlen)
    def record(self,latency_ms,error=False): self.latencies.append(float(latency_ms));self.errors.append(1 if error else 0)
    def snapshot(self):
        xs=sorted(self.latencies)
        def pct(p): return 0.0 if not xs else xs[min(len(xs)-1,max(0,int(p*len(xs))-1))]
        return {"count":len(xs),"p50_ms":pct(.50),"p95_ms":pct(.95),"p99_ms":pct(.99),"error_rate":sum(self.errors)/max(1,len(self.errors))}
