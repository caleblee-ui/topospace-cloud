
from __future__ import annotations
from dataclasses import dataclass, asdict
from collections import deque
from datetime import datetime, timezone

@dataclass
class LiveTopologyFrame:
    seq: int
    event: str
    state_id: str
    nodes: list
    edges: list
    metadata: dict
    timestamp: str

class LiveTraceBuffer:
    def __init__(self, maxlen=1000):
        self.frames=deque(maxlen=maxlen)
        self.seq=0

    def push(self, event, state_id, nodes=None, edges=None, metadata=None):
        self.seq += 1
        frame=LiveTopologyFrame(
            self.seq,event,state_id,nodes or [],edges or [],metadata or {},
            datetime.now(timezone.utc).isoformat()
        )
        self.frames.append(frame)
        return asdict(frame)

    def since(self, seq=0):
        return [asdict(f) for f in self.frames if f.seq > seq]
