
class AdaptiveEpsilonController:
 def __init__(self,min_e=.08,max_e=1.0,target_success=.85):self.min=min_e;self.max=max_e;self.target=target_success
 def update(self,epsilon,recent_success,pressure=0):
  if recent_success<self.target:epsilon*=1.12
  else:epsilon*=.94
  epsilon*=max(.7,1-.12*max(0,pressure))
  return max(self.min,min(self.max,epsilon))
