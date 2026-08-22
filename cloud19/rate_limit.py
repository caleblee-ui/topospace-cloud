
import time
from collections import defaultdict,deque
class SlidingWindowRateLimiter:
    def __init__(self):self.rows=defaultdict(deque)
    def allow(self,key,limit,now=None):
        now=time.time() if now is None else now;q=self.rows[key]
        while q and q[0]<=now-60:q.popleft()
        if len(q)>=limit:return False
        q.append(now);return True
