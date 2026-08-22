
import threading,time
class IdempotencyStore:
    def __init__(self,ttl=300):
        self.ttl=ttl;self.data={};self.lock=threading.RLock()
    def get(self,key):
        with self.lock:
            row=self.data.get(key)
            if not row:return None
            if time.time()-row[0]>self.ttl:
                self.data.pop(key,None);return None
            return row[1]
    def put(self,key,value):
        with self.lock:self.data[key]=(time.time(),value)
