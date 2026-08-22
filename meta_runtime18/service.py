
from meta_policy17.runtime import MetaPolicyRuntime
from meta_policy17.safety import MetaPolicyGuardrail
from online_learning.shadow import ShadowJointEvaluator
from online_learning.promotion import JointPolicyPromotionGate
from online_learning.rollout import StagedRolloutManager
from online_learning.rollback import JointAutomaticRollback

class MetaPolicyProductionRuntime:
    def __init__(self):
        self.champion=MetaPolicyRuntime()
        self.challenger=MetaPolicyRuntime()
        self.guardrail=MetaPolicyGuardrail()
        self.shadow=ShadowJointEvaluator()
        self.promotion=JointPolicyPromotionGate(min_samples=50,min_reward_gain=.01)
        self.rollout=StagedRolloutManager()
        self.rollback=JointAutomaticRollback()
        self.live_metrics={"reward":.70,"success_rate":.95,"violation_rate":0.0,"latency_ms":1000,"sample_count":1000}
        self.challenger_metrics={"reward":0.0,"success_rate":0.0,"violation_rate":0.0,"latency_ms":0.0,"sample_count":0}

    def decide(self,agent_state,routing_ctx):
        live=self.guardrail.apply(agent_state,self.champion.decide(agent_state,routing_ctx))
        shadow=self.guardrail.apply(agent_state,self.challenger.decide(agent_state,routing_ctx))
        return {"live":live,"shadow":shadow}

    def observe(self,champion_score,challenger_score,success=True,violations=0,latency_ms=1000):
        self.shadow.observe(champion_score,challenger_score,violations)
        m=self.challenger_metrics;n=m["sample_count"]+1
        m["reward"]=(m["reward"]*m["sample_count"]+challenger_score)/n
        m["success_rate"]=(m["success_rate"]*m["sample_count"]+(1 if success else 0))/n
        m["violation_rate"]=(m["violation_rate"]*m["sample_count"]+violations)/n
        m["latency_ms"]=(m["latency_ms"]*m["sample_count"]+latency_ms)/n
        m["sample_count"]=n
        return self.shadow.summary()
