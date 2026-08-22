
from optimization_plane.models import ExecutionCandidate
class GeneralGeometryOptimizationBridge:
 def __init__(self,engine):self.engine=engine
 def convert(self,rows):
  out=[]
  for c in rows:
   g=self.engine.distance(c["views"])
   out.append(ExecutionCandidate(c["id"],c.get("kind","memory"),g["distance"],float(c.get("utility",.5)),
    float(c.get("confidence",.5)),int(c.get("token_cost",0)),float(c.get("latency_ms",0)),float(c.get("success_rate",.5)),
    {"geometry_class":g["class"],"guarantees":g["guarantees"],"aggregator":g["aggregator"]}))
  return out
