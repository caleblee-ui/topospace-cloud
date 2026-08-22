
import time
class IdempotencyStore:
 def __init__(self,ttl=3600):self.ttl=ttl;self.data={}
 def get(self,k):
  x=self.data.get(k)
  if not x:return None
  if time.time()-x[0]>self.ttl:self.data.pop(k,None);return None
  return x[1]
 def put(self,k,v):self.data[k]=(time.time(),v)
