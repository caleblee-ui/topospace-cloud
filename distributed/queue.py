
from __future__ import annotations
from queue import Queue, Empty
from threading import Thread, Event
import uuid

class WorkerQueue:
    def __init__(self,workers=4):
        self.q=Queue();self.stop_event=Event();self.results={};self.threads=[]
        for i in range(workers):
            t=Thread(target=self._run,name=f"topospace-worker-{i}",daemon=True);t.start();self.threads.append(t)
    def submit(self,fn,*args,**kwargs):
        jid=uuid.uuid4().hex;self.q.put((jid,fn,args,kwargs));return jid
    def _run(self):
        while not self.stop_event.is_set():
            try:jid,fn,args,kwargs=self.q.get(timeout=.2)
            except Empty:continue
            try:self.results[jid]={"done":True,"result":fn(*args,**kwargs),"error":None}
            except Exception as e:self.results[jid]={"done":True,"result":None,"error":str(e)}
            finally:self.q.task_done()
    def get(self,jid):return self.results.get(jid,{"done":False})
    def shutdown(self):self.stop_event.set()
