
import math
class AdmissibleAggregator:
 name="admissible"
 def aggregate(self,v,w=None):raise NotImplementedError
 def __call__(self,v,w=None):return self.aggregate(v,w)
 def validate_axioms(self,tol=1e-9):
  samples=[([.1,.2],[.3,.4]),([.2,.0],[.4,.1]),([.0,.5],[.6,.7])]
  if abs(self.aggregate([0,0]))>tol:return False
  for u,v in samples:
   if self.aggregate(u)>self.aggregate(v)+tol:return False
   uv=[a+b for a,b in zip(u,v)]
   if self.aggregate(uv)>self.aggregate(u)+self.aggregate(v)+tol:return False
  return True

class WeightedLp(AdmissibleAggregator):
 def __init__(self,p=2):
  if p<1:raise ValueError("p_must_be_at_least_1")
  self.p=float(p);self.name=f"weighted_lp_{self.p:g}"
 def aggregate(self,v,w=None):
  if not v:return 0.0
  w=w or [1/len(v)]*len(v)
  if math.isinf(self.p):return max(x for x,wi in zip(v,w) if wi>0)
  return sum(max(0,wi)*max(0,x)**self.p for x,wi in zip(v,w))**(1/self.p)

class WeightedChebyshev(AdmissibleAggregator):
 name="weighted_chebyshev"
 def aggregate(self,v,w=None):
  if not v:return 0.0
  w=w or [1]*len(v)
  return max(max(0,wi)*max(0,x) for x,wi in zip(v,w))

class ConicCombination(AdmissibleAggregator):
 name="conic_combination"
 def __init__(self,parts,coeffs):self.parts=parts;self.coeffs=coeffs
 def aggregate(self,v,w=None):return sum(max(0,c)*a.aggregate(v,w) for a,c in zip(self.parts,self.coeffs))

class MaxAggregator(AdmissibleAggregator):
 name="max_aggregator"
 def __init__(self,parts):self.parts=parts
 def aggregate(self,v,w=None):return max((a.aggregate(v,w) for a in self.parts),default=0)

class ConcaveReshape(AdmissibleAggregator):
 name="concave_reshape"
 def __init__(self,base,kind="fraction",lam=1):self.base=base;self.kind=kind;self.lam=float(lam)
 def aggregate(self,v,w=None):
  x=self.base.aggregate(v,w)
  if self.kind=="fraction":return x/(1+x)
  if self.kind=="exp":return 1-math.exp(-self.lam*x)
  if self.kind=="clip":return min(x,1)
  raise ValueError("unknown_reshape")

class OrderedWeightedAverage(AdmissibleAggregator):
 name="owa"
 def __init__(self,omega):
  if any(omega[i]<omega[i+1] for i in range(len(omega)-1)):raise ValueError("weights_nonincreasing_required")
  self.omega=list(omega)
 def aggregate(self,v,w=None):
  xs=sorted([max(0,x) for x in v],reverse=True)
  om=self.omega+[0]*max(0,len(xs)-len(self.omega))
  return sum(a*b for a,b in zip(om,xs))

class NestedAggregator(AdmissibleAggregator):
 name="nested"
 def __init__(self,groups,outer):self.groups=groups;self.outer=outer
 def aggregate(self,v,w=None):
  inner=[agg.aggregate([v[i] for i in idx],gw) for idx,agg,gw in self.groups]
  return self.outer.aggregate(inner,None)
