
from __future__ import annotations
from topology.persistence import zero_dim_persistence

class PersistentContextSelector:
    """Ranks candidate objects by structural persistence across epsilon scales."""

    def rank(self, nodes, weighted_edges):
        intervals=zero_dim_persistence(nodes, weighted_edges)
        score={n:0.0 for n in nodes}
        for iv in intervals:
            score[iv.component] = 1e9 if iv.death is None else float(iv.persistence or 0.0)
        return sorted(score.items(), key=lambda x:x[1], reverse=True)
