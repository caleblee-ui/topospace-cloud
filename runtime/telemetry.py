from contextlib import contextmanager
from time import perf_counter
from collections import defaultdict
class Telemetry:
 def __init__(self):self.counters=defaultdict(int);self.timings=defaultdict(list)
 def count(self,n,v=1):self.counters[n]+=v
 @contextmanager
 def timer(self,n):
  s=perf_counter()
  try:yield
  finally:self.timings[n].append(perf_counter()-s)
 def snapshot(self):return {'counters':dict(self.counters),'timings':{k:{'count':len(v),'mean_ms':sum(v)/len(v)*1000 if v else 0} for k,v in self.timings.items()}}
