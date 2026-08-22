
class TopologicalCostScorer:
 def score(self,x,budget):
  proximity=1-min(1,max(0,x.distance/max(.0001,budget.epsilon)))
  token_eff=1-min(1,x.token_cost/max(1,budget.max_tokens))
  latency_eff=1-min(1,x.latency_ms/max(1,budget.max_latency_ms))
  return .25*proximity+.22*x.utility+.18*x.confidence+.17*x.success_rate+.10*token_eff+.08*latency_eff
