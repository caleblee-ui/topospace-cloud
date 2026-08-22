
from general_geometry.classes import combined_class,GUARANTEES
class GeneralizedGeometryEngine:
 def __init__(self,aggregator):self.aggregator=aggregator
 def distance(self,views):
  d=self.aggregator.aggregate([max(0,float(x.value)) for x in views],[max(0,float(x.weight)) for x in views])
  cls=combined_class([x.distance_class for x in views])
  return {"distance":d,"class":cls.value,"guarantees":sorted(GUARANTEES[cls.value]),"aggregator":self.aggregator.name}
 def neighborhood(self,candidates,epsilon):
  rows=[]
  for c in candidates:
   g=self.distance(c["views"])
   if g["distance"]<epsilon:rows.append({**c,"geometry":g})
  return sorted(rows,key=lambda x:x["geometry"]["distance"])
