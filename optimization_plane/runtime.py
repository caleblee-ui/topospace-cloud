
from optimization_plane.optimizer import TopologyOptimizer
from optimization_plane.adaptive import AdaptiveEpsilonController
from optimization_plane.context import ContextCompactor
from optimization_plane.learning import OutcomeLearner
class OptimizationPlane:
 def __init__(self):
  self.optimizer=TopologyOptimizer();self.epsilon=AdaptiveEpsilonController();self.context=ContextCompactor();self.learning=OutcomeLearner()
 def plan(self,candidates,budget,context_items=None):
  self.learning.apply(candidates)
  plan=self.optimizer.optimize(candidates,budget)
  if context_items is not None:plan["context"]=self.context.compact(context_items,budget.max_tokens)
  return plan
 def feedback(self,selected,reward):
  for x in selected:self.learning.record(x.id,reward)
