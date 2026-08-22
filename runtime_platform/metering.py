
from collections import defaultdict
class UsageMeter:
 def __init__(self):self.v=defaultdict(lambda:defaultdict(float))
 def record(self,t,m,a=1):self.v[t][m]+=a
 def snapshot(self,t):return dict(self.v[t])
