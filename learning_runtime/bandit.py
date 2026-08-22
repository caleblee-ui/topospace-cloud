
from __future__ import annotations
import math, random
from dataclasses import dataclass, field

@dataclass
class ArmStats:
    pulls:int=0
    reward_sum:float=0.0
    success_sum:float=0.0

    @property
    def mean_reward(self): return self.reward_sum/max(1,self.pulls)
    @property
    def success_rate(self): return self.success_sum/max(1,self.pulls)

class ContextualBandit:
    """Lightweight UCB bandit keyed by coarse task context bucket."""
    def __init__(self, arms, exploration=1.2):
        self.arms=list(arms)
        self.exploration=exploration
        self.stats={}

    @staticmethod
    def bucket(context):
        c=context or {}
        return (
          "hi_u" if float(c.get("uncertainty",.3))>.6 else "lo_u",
          "hi_c" if float(c.get("complexity",.5))>.6 else "lo_c",
          "hi_p" if float(c.get("cost_pressure",.5))>.6 else "lo_p",
        )

    def _row(self,bucket,arm):
        return self.stats.setdefault((bucket,arm),ArmStats())

    def select(self,context):
        b=self.bucket(context)
        total=sum(self._row(b,a).pulls for a in self.arms)+1
        for a in self.arms:
            if self._row(b,a).pulls==0:return a
        def ucb(a):
            s=self._row(b,a)
            return s.mean_reward+self.exploration*math.sqrt(math.log(total)/s.pulls)
        return max(self.arms,key=ucb)

    def update(self,context,arm,reward,success):
        b=self.bucket(context);s=self._row(b,arm)
        s.pulls+=1;s.reward_sum+=float(reward);s.success_sum+=1.0 if success else 0.0
