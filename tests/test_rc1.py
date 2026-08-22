
from online_learning.promotion import JointPolicyPromotionGate
from online_learning.models import PolicySnapshot
from online_learning.rollback import JointAutomaticRollback
from online_learning.rollout import StagedRolloutManager
from online_learning.service import SafeOnlineJointRuntime

def test_promotion_gate():
    c=PolicySnapshot("c",1,.70,.95,0.0,10,1000)
    x=PolicySnapshot("x",2,.74,.95,0.0,10.5,100)
    assert JointPolicyPromotionGate().evaluate(c,x)["promote"]

def test_violation_blocks_promotion():
    c=PolicySnapshot("c",1,.70,.95,0.0,10,1000)
    x=PolicySnapshot("x",2,.80,.98,.01,10,100)
    assert not JointPolicyPromotionGate().evaluate(c,x)["promote"]

def test_staged_rollout():
    r=StagedRolloutManager()
    assert r.start()==5 and r.advance()==25 and r.advance()==50 and r.advance()==100

def test_rollback():
    rb=JointAutomaticRollback()
    assert rb.check({"reward":.8,"latency_ms":10},{"reward":.7,"latency_ms":10})["rollback"]

def test_shadow_stats():
    s=SafeOnlineJointRuntime()
    for i in range(60):
        s.observe(.7,.75,True,0,10)
    out=s.promotion_check()
    assert out["promote"]
