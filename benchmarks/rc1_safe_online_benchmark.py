
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from online_learning.service import SafeOnlineJointRuntime

r=SafeOnlineJointRuntime()
for i in range(200):
    r.observe(.70,.74 if i<150 else .76,True,0,10.2)

shadow=r.shadow.summary()
promotion=r.promotion_check()

# Simulate rollout health and rollback decision.
baseline={"reward":.74,"latency_ms":10.2,"error_rate":.01,"violation_rate":0.0}
healthy={"reward":.75,"latency_ms":10.5,"error_rate":.01,"violation_rate":0.0}
bad={"reward":.66,"latency_ms":13.0,"error_rate":.08,"violation_rate":.0}

out={
 "shadow_samples":shadow["samples"],
 "challenger_win_rate":shadow["challenger_win_rate"],
 "mean_shadow_gain":shadow["mean_gain"],
 "promotion":promotion,
 "healthy_rollback":r.rollback.check(baseline,healthy),
 "bad_rollback":r.rollback.check(baseline,bad)
}
print(json.dumps(out,indent=2))
assert promotion["promote"]
assert out["healthy_rollback"]["rollback"] is False
assert out["bad_rollback"]["rollback"] is True
Path("results/rc1_safe_online_benchmark.json").write_text(json.dumps(out,indent=2))
