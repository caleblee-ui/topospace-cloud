
from __future__ import annotations
from topology.drift import TopologicalDrift

class DriftAwareReplanner:
    def __init__(self, threshold: float = 0.35):
        self.threshold=threshold
        self.detector=TopologicalDrift()

    def should_replan(self, previous, current):
        report=self.detector.compare(previous,current)
        return report.score >= self.threshold, report
