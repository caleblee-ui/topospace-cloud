
from __future__ import annotations
import math

class ConceptDriftDetector:
    """Population Stability Index over bucketed scalar signals."""
    def __init__(self,bins=10,threshold=.20):
        self.bins=bins;self.threshold=threshold

    def _hist(self,values):
        h=[0]*self.bins
        for v in values:
            i=min(self.bins-1,max(0,int(float(v)*self.bins)))
            h[i]+=1
        total=max(1,sum(h))
        return [max(1e-6,x/total) for x in h]

    def psi(self,reference,current):
        a=self._hist(reference);b=self._hist(current)
        return sum((y-x)*math.log(y/x) for x,y in zip(a,b))

    def detect(self,reference,current):
        value=self.psi(reference,current)
        return {"drift":value>=self.threshold,"psi":value,"threshold":self.threshold}
