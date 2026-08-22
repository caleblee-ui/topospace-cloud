
from general_geometry.aggregators import WeightedLp,WeightedChebyshev,NestedAggregator
def exploratory_profile():return WeightedLp(1)
def balanced_profile():return WeightedLp(2)
def hard_constraint_profile():return WeightedChebyshev()
def hierarchical_agent_profile():
 return NestedAggregator([
  ([0,1,2],WeightedLp(1),[.45,.3,.25]),
  ([3,4],WeightedChebyshev(),[1,1]),
  ([5,6],WeightedLp(2),[.5,.5])
 ],WeightedLp(2))
