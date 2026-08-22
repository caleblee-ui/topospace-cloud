
from __future__ import annotations
import statistics, math, random

def mean(xs): return statistics.mean(xs) if xs else 0.0

def bootstrap_ci(values, statistic=None, confidence=.95, samples=2000, seed=7):
    if not values: return (0.0,0.0)
    statistic=statistic or mean
    rng=random.Random(seed); n=len(values); boots=[]
    for _ in range(samples):
        boots.append(statistic([values[rng.randrange(n)] for _ in range(n)]))
    boots.sort()
    alpha=(1-confidence)/2
    lo=boots[int(alpha*samples)]
    hi=boots[min(samples-1,int((1-alpha)*samples)-1)]
    return (lo,hi)

def paired_reduction(base,opt):
    out=[]
    for b,o in zip(base,opt):
        if b>0: out.append(100*(1-o/b))
    return out

def paired_delta(base,opt):
    return [o-b for b,o in zip(base,opt)]
