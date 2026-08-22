
from optimization_plane.scorer import TopologicalCostScorer
class TopologyOptimizer:
 def __init__(self):self.scorer=TopologicalCostScorer()
 def optimize(self,candidates,budget):
  eligible=[x for x in candidates if x.distance<=budget.epsilon]
  ranked=sorted(eligible,key=lambda x:self.scorer.score(x,budget),reverse=True)
  chosen=[];tokens=0;latency=0
  for x in ranked:
   if len([y for y in chosen if y.kind=="tool"])>=budget.max_tool_calls and x.kind=="tool":continue
   if tokens+x.token_cost>budget.max_tokens:continue
   if latency+x.latency_ms>budget.max_latency_ms:continue
   chosen.append(x);tokens+=x.token_cost;latency+=x.latency_ms
  return {"selected":chosen,"tokens":tokens,"latency_ms":latency,
          "scores":{x.id:self.scorer.score(x,budget) for x in ranked}}
