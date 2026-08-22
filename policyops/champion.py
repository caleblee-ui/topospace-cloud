
from dataclasses import dataclass

@dataclass
class PolicyCandidate:
    name:str
    version:int
    reward:float
    success_rate:float
    risk:float
    sample_count:int

class ChampionChallenger:
    def __init__(self,min_samples=30,min_reward_gain=.03,max_success_drop=.01,max_risk=.75):
        self.min_samples=min_samples
        self.min_reward_gain=min_reward_gain
        self.max_success_drop=max_success_drop
        self.max_risk=max_risk

    def evaluate(self,champion:PolicyCandidate,challenger:PolicyCandidate):
        reasons=[]
        if challenger.sample_count<self.min_samples:reasons.append("insufficient_samples")
        if challenger.reward < champion.reward+self.min_reward_gain:reasons.append("reward_gain_too_small")
        if challenger.success_rate < champion.success_rate-self.max_success_drop:reasons.append("success_guardrail")
        if challenger.risk>self.max_risk:reasons.append("risk_guardrail")
        return {"promote":not reasons,"reasons":reasons}
