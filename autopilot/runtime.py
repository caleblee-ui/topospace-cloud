
from __future__ import annotations
from collections import deque
from autopilot.models import RuntimeSignals
from autopilot.controller import TopologyAutopilot
from autopilot.policy import AutopilotPolicy

class AutopilotRuntime:
    def __init__(self,controller=None,policy=None,window=50):
        self.controller=controller or TopologyAutopilot()
        self.policy=policy or AutopilotPolicy()
        self.history=deque(maxlen=window)
        self.previous=None

    def update(self,signals:RuntimeSignals):
        raw=self.controller.decide(signals)
        safe=self.policy.apply(self.previous,raw)
        self.previous=safe
        row={"signals":signals.__dict__.copy(),"decision":safe.to_dict()}
        self.history.append(row)
        return row

    def recent(self): return list(self.history)
