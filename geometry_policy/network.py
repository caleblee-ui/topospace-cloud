
import math
from geometry_policy.model import GeometryDecision

def _softmax(xs):
    m=max(xs); es=[math.exp(x-m) for x in xs]; s=sum(es)
    return [x/s for x in es]

class GeometryPolicyNetwork:
    """
    Lightweight dependency-free policy head.
    It learns/selects the geometry family rather than only p.
    This reference implementation is trainable with bandit-style reward updates.
    """
    families=("lp","chebyshev","owa","nested")

    def __init__(self,n_views=7,seed=1729):
        import random
        r=random.Random(seed)
        self.n_views=n_views
        self.family_w={f:[r.uniform(-.05,.05) for _ in range(6)] for f in self.families}
        self.view_logits=[0.0]*n_views
        self.p_raw=0.0
        self.eps_raw=0.0

    def features(self,s):
        return [1.0,float(s.risk),float(s.ambiguity),float(s.hierarchy),
                float(s.candidate_pressure),float(s.latency_pressure)]

    def decide(self,s):
        x=self.features(s)
        # Strong inductive priors matching the paper/runtime semantics.
        scores={}
        for f in self.families:
            scores[f]=sum(a*b for a,b in zip(self.family_w[f],x))
        scores["chebyshev"] += 2.2*s.risk
        scores["nested"] += 1.7*s.hierarchy + .8*s.risk
        scores["lp"] += 1.2*s.ambiguity
        scores["owa"] += .8*s.candidate_pressure
        probs=_softmax([scores[f] for f in self.families])
        family=self.families[max(range(len(probs)),key=lambda i:probs[i])]
        vw=_softmax(self.view_logits)
        p=1.0+3.0/(1.0+math.exp(-self.p_raw))
        eps=.15+.75/(1.0+math.exp(-self.eps_raw))
        return GeometryDecision(family,vw,eps,p,max(probs),dict(zip(self.families,probs)))

    def update(self,s,decision,reward,lr=.03):
        x=self.features(s)
        # REINFORCE-like family update with deterministic chosen action.
        for f in self.families:
            target=1.0 if f==decision.aggregator else 0.0
            prob=decision.scores.get(f,0.0)
            grad=(target-prob)*reward
            self.family_w[f]=[w+lr*grad*xi for w,xi in zip(self.family_w[f],x)]
        # bounded scalar heads
        self.eps_raw += lr*reward*(0.5-decision.epsilon)
        self.p_raw += lr*reward*(2.0-decision.p)*.1
