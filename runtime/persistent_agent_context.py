
from __future__ import annotations
from topology.persistent_homology import PersistentHomologySummary
from runtime.persistent_context import PersistentContextSelector

class PersistentAgentContext:
    """Combines persistent 0D ranking with H0/H1 multi-scale diagnostics."""
    def __init__(self):
        self.selector=PersistentContextSelector()
        self.ph=PersistentHomologySummary()

    def build(self,nodes,weighted_edges,epsilons):
        ranking=self.selector.rank(nodes,weighted_edges)
        summary=self.ph.compute(nodes,weighted_edges,epsilons)
        return {
            "ranking":ranking,
            "homology":summary,
            "stable_h1":self.ph.stable_h1(summary)
        }
