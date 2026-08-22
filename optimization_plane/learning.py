
from collections import defaultdict
class OutcomeLearner:
 def __init__(self):self.stats=defaultdict(lambda:{"n":0,"reward":0.0})
 def record(self,candidate_id,reward):
  s=self.stats[candidate_id];s["n"]+=1;s["reward"]+=float(reward)
 def mean(self,candidate_id):
  s=self.stats[candidate_id];return s["reward"]/s["n"] if s["n"] else .5
 def apply(self,candidates):
  for x in candidates:
   if self.stats[x.id]["n"]:x.success_rate=self.mean(x.id)
  return candidates
