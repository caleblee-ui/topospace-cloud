
import heapq
class ChainDistance:
 def shortest(self,nodes,local_distance,source,target):
  q=[(0.0,source)];best={source:0.0}
  while q:
   d,u=heapq.heappop(q)
   if u==target:return d
   if d!=best[u]:continue
   for v in nodes:
    if v==u:continue
    nd=d+float(local_distance(u,v))
    if nd<best.get(v,float("inf")):best[v]=nd;heapq.heappush(q,(nd,v))
  return float("inf")
