from math import inf
from typing import Sequence


def weighted_lp(a: Sequence[float], b: Sequence[float], p: float = 2.0, weights=None) -> float:
    if len(a) != len(b):
        raise ValueError('dimension mismatch')
    if p < 1:
        raise ValueError('p must be >= 1 for a metric')
    if weights is None:
        weights = [1.0] * len(a)
    if len(weights) != len(a):
        raise ValueError('weight dimension mismatch')
    if p == inf:
        return max((w * abs(x-y) for x, y, w in zip(a, b, weights)), default=0.0)
    return sum(w * (abs(x-y) ** p) for x, y, w in zip(a, b, weights)) ** (1.0/p)
