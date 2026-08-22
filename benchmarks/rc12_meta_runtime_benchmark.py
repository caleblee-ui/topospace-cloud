
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from meta_runtime18.service import MetaPolicyProductionRuntime
from meta_runtime18.promotion import MetaPromotionAdapter

r=MetaPolicyProductionRuntime()
for i in range(250):
    r.observe(.70,.745 if i<180 else .76,True,0,970)

promotion=MetaPromotionAdapter().check(r)
healthy=r.rollback.check(
 {"reward":.745,"latency_ms":970,"error_rate":.01,"violation_rate":0.0},
 {"reward":.75,"latency_ms":990,"error_rate":.01,"violation_rate":0.0}
)
bad=r.rollback.check(
 {"reward":.745,"latency_ms":970,"error_rate":.01,"violation_rate":0.0},
 {"reward":.66,"latency_ms":1300,"error_rate":.08,"violation_rate":0.0}
)

out={"shadow":r.shadow.summary(),"promotion":promotion,
     "healthy_rollback":healthy,"bad_rollback":bad}
print(json.dumps(out,indent=2))
assert promotion["promote"]
assert healthy["rollback"] is False
assert bad["rollback"] is True
Path("results/rc12_meta_runtime_benchmark.json").write_text(json.dumps(out,indent=2))
