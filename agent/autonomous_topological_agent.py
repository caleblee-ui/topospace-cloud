
from __future__ import annotations
from runtime.closed_loop import ClosedLoopTopoAgent

class AutonomousTopologicalAgent:
    """Thin product-facing facade around the closed-loop runtime."""
    def __init__(self, runtime=None):
        self.runtime=runtime or ClosedLoopTopoAgent()

    def execute(self, objective, candidates, edges, executor, mutate=None):
        return self.runtime.run(objective,candidates,edges,executor,mutate)
