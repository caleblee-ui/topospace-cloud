
import time,uuid
class Tracer:
 def __init__(self):self.spans=[]
 def start(self,n,a=None):
  s={"name":n,"attrs":a or {},"trace_id":uuid.uuid4().hex,"start":time.perf_counter()};self.spans.append(s);return s
 def finish(self,s):s["duration_ms"]=(time.perf_counter()-s["start"])*1000
