
import queue
class TopologyEventStream:
 def __init__(self):self.s={}
 def subscribe(self,t):q=queue.Queue();self.s.setdefault(t,[]).append(q);return q
 def publish(self,t,e):
  for q in self.s.get(t,[]):q.put_nowait(e)
