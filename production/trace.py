
import uuid,time
class RequestTrace:
    def __init__(self,trace_id=None):
        self.trace_id=trace_id or uuid.uuid4().hex;self.started=time.time();self.events=[]
    def add(self,event,**data):self.events.append({"ts":time.time(),"event":event,**data})
    def finish(self):return {"trace_id":self.trace_id,"elapsed_ms":(time.time()-self.started)*1000,"events":self.events}
