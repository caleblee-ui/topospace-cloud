
from __future__ import annotations
import math,statistics

class DynamicPNorm:
    """Chooses p from workload dispersion, then computes weighted Lp distance."""
    def choose_p(self,vectors):
        if not vectors or len(vectors)<2:return 2.0
        dims=len(vectors[0]);vars=[]
        for j in range(dims):
            col=[float(v[j]) for v in vectors]
            vars.append(statistics.pvariance(col))
        dispersion=sum(vars)/max(1,len(vars))
        if dispersion<.015:return 1.25
        if dispersion<.06:return 1.75
        if dispersion<.15:return 2.0
        return 3.0

    def distance(self,a,b,p=2.0,weights=None):
        if len(a)!=len(b):raise ValueError("dimension_mismatch")
        w=weights or [1.0]*len(a)
        return sum(float(wi)*abs(float(x)-float(y))**p for x,y,wi in zip(a,b,w))**(1.0/p)

class AdaptiveEpsilon:
    """Selects epsilon from nearest-neighbor distance distribution."""
    def choose(self,distances,target_fraction=.25,min_epsilon=.05,max_epsilon=.8):
        if not distances:return min_epsilon
        ds=sorted(max(0.0,float(x)) for x in distances)
        idx=min(len(ds)-1,max(0,int(round((len(ds)-1)*target_fraction))))
        return max(min_epsilon,min(max_epsilon,ds[idx]))
