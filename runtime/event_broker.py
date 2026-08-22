
from __future__ import annotations
from collections import defaultdict
from threading import Condition
import time

class EventBroker:
    """In-process workspace event broker for reference deployments."""
    def __init__(self, max_events=1000):
        self.max_events=max_events
        self.events=defaultdict(list)
        self.cv=Condition()

    def publish(self, workspace_id, frame):
        with self.cv:
            bucket=self.events[workspace_id]
            bucket.append(frame)
            if len(bucket)>self.max_events:
                del bucket[:-self.max_events]
            self.cv.notify_all()

    def since(self, workspace_id, seq=0):
        with self.cv:
            return [f for f in self.events.get(workspace_id,[]) if int(f.get("seq",0))>int(seq)]

    def wait_since(self, workspace_id, seq=0, timeout=15.0):
        deadline=time.time()+timeout
        with self.cv:
            while True:
                rows=[f for f in self.events.get(workspace_id,[]) if int(f.get("seq",0))>int(seq)]
                if rows:return rows
                remain=deadline-time.time()
                if remain<=0:return []
                self.cv.wait(remain)
