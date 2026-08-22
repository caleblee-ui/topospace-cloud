
from general_geometry.aggregators import WeightedLp, WeightedChebyshev, OrderedWeightedAverage, NestedAggregator

class GeometryCompiler:
    def compile(self,decision):
        if decision.aggregator=="lp":
            return WeightedLp(decision.p)
        if decision.aggregator=="chebyshev":
            return WeightedChebyshev()
        if decision.aggregator=="owa":
            # worst views dominate
            n=len(decision.weights)
            omega=[(n-i) for i in range(n)]
            z=sum(omega)
            return OrderedWeightedAverage([x/z for x in omega])
        if decision.aggregator=="nested":
            n=len(decision.weights)
            # standard 7-view profile; safe fallback for arbitrary view count
            if n>=7:
                return NestedAggregator([
                    ([0,1,2],WeightedLp(1),decision.weights[:3]),
                    ([3,4],WeightedChebyshev(),[1,1]),
                    ([5,6],WeightedLp(2),decision.weights[5:7])
                ],WeightedLp(2))
            return WeightedLp(decision.p)
        raise ValueError("unknown_geometry_family")
