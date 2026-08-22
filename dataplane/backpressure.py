
import threading,time
class BackpressureController:
    def __init__(self,max_inflight=128,queue_threshold=256):
        self.max_inflight=max_inflight;self.queue_threshold=queue_threshold
        self.inflight=0;self.queued=0;self.lock=threading.RLock()
    def admit(self):
        with self.lock:
            if self.inflight>=self.max_inflight:
                if self.queued>=self.queue_threshold:return {"ok":False,"reason":"overloaded"}
                self.queued+=1;return {"ok":True,"queued":True}
            self.inflight+=1;return {"ok":True,"queued":False}
    def start_queued(self):
        with self.lock:
            if self.queued>0 and self.inflight<self.max_inflight:
                self.queued-=1;self.inflight+=1;return True
            return False
    def release(self):
        with self.lock:self.inflight=max(0,self.inflight-1)
    def snapshot(self):
        with self.lock:return {"inflight":self.inflight,"queued":self.queued}
