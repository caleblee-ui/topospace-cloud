
import time
class TokenBucket:
 def __init__(self,rate=10000,burst=10000):self.rate=rate;self.burst=burst;self.state={}
 def allow(self,k,cost=1):
  now=time.monotonic();tokens,last=self.state.get(k,(self.burst,now));tokens=min(self.burst,tokens+(now-last)*self.rate);ok=tokens>=cost
  if ok:tokens-=cost
  self.state[k]=(tokens,now);return ok
