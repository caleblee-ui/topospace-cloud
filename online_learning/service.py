
from joint_optimizer.runtime import JointGeometryRuntime
from online_learning.shadow import ShadowJointEvaluator
from online_learning.promotion import JointPolicyPromotionGate
from online_learning.rollout import StagedRolloutManager
from online_learning.rollback import JointAutomaticRollback
from online_learning.models import PolicySnapshot

class SafeOnlineJointRuntime:
    """
    Production-facing orchestration around JointGeometryRuntime.
    Champion handles live execution; challenger runs shadow until promotion gates pass.
    """
    def __init__(self):
        self.champion=JointGeometryRuntime()
        self.challenger=JointGeometryRuntime()
        self.shadow=ShadowJointEvaluator()
        self.promotion=JointPolicyPromotionGate()
        self.rollout=StagedRolloutManager()
        self.rollback=JointAutomaticRollback()
        self.champion_stats=PolicySnapshot("champion",1,.70,.95,0.0,10.0,1000)
        self.challenger_stats=PolicySnapshot("challenger",1,.0,.0,0.0,0.0,0)

    def execute(self,state,spaces):
        live=self.champion.solve(state,spaces)
        shadow=self.challenger.solve(state,spaces)
        return {"live":live,"shadow":shadow}

    def observe(self,champion_score,challenger_score,success=True,violations=0,latency_ms=10.0):
        self.shadow.observe(champion_score,challenger_score,violations)
        c=self.challenger_stats
        n=c.sample_count+1
        c.reward=(c.reward*c.sample_count+challenger_score)/n
        c.success_rate=(c.success_rate*c.sample_count+(1 if success else 0))/n
        c.violation_rate=(c.violation_rate*c.sample_count+violations)/n
        c.latency_ms=(c.latency_ms*c.sample_count+latency_ms)/n
        c.sample_count=n
        return self.shadow.summary()

    def promotion_check(self):
        return self.promotion.evaluate(self.champion_stats,self.challenger_stats)
