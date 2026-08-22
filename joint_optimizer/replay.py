
class JointReplayBuffer:
    def __init__(self,maxlen=5000):self.maxlen=maxlen;self.rows=[]
    def add(self,state,rewards,score):
        self.rows.append((state,rewards,float(score)))
        if len(self.rows)>self.maxlen:self.rows=self.rows[-self.maxlen:]
    def sample(self,n):
        import random
        if not self.rows:return []
        return random.sample(self.rows,min(n,len(self.rows)))
