
from __future__ import annotations
import json, time
from runtime.live_trace import LiveTraceBuffer

class SSEStream:
    def __init__(self, buffer: LiveTraceBuffer):
        self.buffer=buffer

    def poll(self, since=0):
        return self.buffer.since(since)

    @staticmethod
    def encode(frame):
        return "event: topology\\ndata: "+json.dumps(frame)+"\\n\\n"
