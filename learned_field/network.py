
import math,random
from learned_field.models import FieldSnapshot

DOMAINS=("memory","tool","skill","plan")

def sigmoid(x): return 1/(1+math.exp(-x))

class CouplingFieldNetwork:
    """State-conditioned coupling field C_theta(s)."""
    def __init__(self,seed=1729):
        rng=random.Random(seed)
        self.features=8
        self.weights={}
        for src in DOMAINS:
            self.weights[src]={}
            for dst in DOMAINS:
                if src==dst:continue
                self.weights[src][dst]=[rng.uniform(-.05,.05) for _ in range(self.features)]
        self.bias={
          "memory":{"tool":.28,"skill":.18,"plan":.32},
          "tool":{"memory":.12,"skill":.20,"plan":.36},
          "skill":{"memory":.10,"tool":.24,"plan":.25},
          "plan":{"memory":.18,"tool":.30,"skill":.16},
        }

    def x(self,s):
        return [1.0,s.risk,s.ambiguity,s.hierarchy,s.candidate_pressure,
                s.latency_pressure,s.memory_pressure,s.tool_pressure]

    def forward(self,s):
        x=self.x(s)
        out={};confs=[]
        for src in DOMAINS:
            out[src]={}
            for dst,w in self.weights[src].items():
                raw=sum(a*b for a,b in zip(w,x))
                # stateful modifiers as inductive priors
                prior=self.bias[src][dst]
                if src=="memory" and dst=="plan": raw += 1.0*s.hierarchy
                if src=="tool" and dst=="plan": raw += .8*s.risk
                if src=="tool" and dst=="skill": raw += .6*s.tool_pressure
                if src=="memory" and dst=="tool": raw += .5*s.memory_pressure
                v=max(-.5,min(.8, prior + .5*(sigmoid(raw)-.5)))
                out[src][dst]=v
                confs.append(abs(sigmoid(raw)-.5)*2)
        return FieldSnapshot(out,sum(confs)/max(1,len(confs)))

    def update(self,s,rewards,lr=.03):
        x=self.x(s)
        snap=self.forward(s)
        for src,row in self.weights.items():
            sr=float(rewards.get(src,0))
            for dst,w in row.items():
                dr=float(rewards.get(dst,0))
                target=sr*dr
                pred=snap.couplings[src][dst]
                err=target-pred
                self.weights[src][dst]=[wi+lr*err*xi for wi,xi in zip(w,x)]
        return self.forward(s)
