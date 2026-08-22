
from __future__ import annotations
import math

def weighted_lp_batch(query, matrix, weights=None, p=2.0):
    """Dependency-free batch weighted Lp; optimized to avoid per-row object allocation."""
    if weights is None:weights=[1.0]*len(query)
    inv=1.0/float(p)
    out=[]
    q=query;w=weights
    for row in matrix:
        s=0.0
        for i,x in enumerate(row):
            s += w[i]*abs(q[i]-x)**p
        out.append(s**inv)
    return out
