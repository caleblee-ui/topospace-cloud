
from __future__ import annotations
from topology.homology import betti_numbers

class PersistentHomologySummary:
    """Tracks H0/H1 summaries across epsilon scales.

    This is a transparent reference implementation suitable for agent diagnostics.
    Production-scale PH should use a specialized backend behind this interface.
    """
    def compute(self, nodes, weighted_edges, epsilons):
        out=[]
        for eps in sorted(epsilons):
            b=betti_numbers(nodes,weighted_edges,eps)
            out.append({"epsilon":float(eps),**b})
        return out

    def stable_h1(self, summary):
        runs=[]; start=None; last=None
        for row in summary:
            if row["beta1"]>0:
                if start is None:start=row["epsilon"]
                last=row["epsilon"]
            elif start is not None:
                runs.append((start,last));start=None;last=None
        if start is not None:runs.append((start,last))
        return runs
