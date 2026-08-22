import math
def cosine(a,b):
 dot=sum(x*y for x,y in zip(a,b));na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(y*y for y in b));return dot/(na*nb) if na and nb else 0.0
class ANNIndex:
 def __init__(self,dim):self.dim=dim;self._vectors={};self.backend='exact'
 def build(self,items):self._vectors=dict(items)
 def query(self,vector,k=20):return sorted(((key,cosine(vector,val)) for key,val in self._vectors.items()),key=lambda x:x[1],reverse=True)[:k]
