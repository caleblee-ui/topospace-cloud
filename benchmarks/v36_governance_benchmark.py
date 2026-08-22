
from pathlib import Path
import sys,json,time,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from governance.manager import PolicyGovernanceManager
from replication.policy_replication import MultiRegionPolicyReplicator
from dr.policy_backup import PolicyDisasterRecovery

g=PolicyGovernanceManager("secret",required_approvals=2)
submission=g.submit("req1","tenant-a","coding",7,{"profile":"efficient","epsilon":.28},"alice")
g.approvals.approve("req1","bob")
scheduled=g.approve_and_schedule("req1","carol",time.time()-1,10)
due=g.scheduler.due()

rep=MultiRegionPolicyReplicator(["seoul","tokyo","singapore"])
rep_result=rep.replicate("tenant-a:coding:v7",submission["signed"]["envelope"])

with tempfile.TemporaryDirectory() as d:
    path=Path(d)/"dr.json"
    dr=PolicyDisasterRecovery()
    bundle=dr.export_bundle(path,[submission["signed"]["envelope"]],g.lineage.history("tenant-a","coding"))
    restored=dr.restore_bundle(path)

out={
 "approved":scheduled["approved"],
 "due_rollouts":due,
 "replicated":rep.verify("tenant-a:coding:v7"),
 "regions":rep_result["regions"],
 "dr_restore_count":len(restored["policies"]),
}
print(json.dumps(out,indent=2))
assert out["approved"] and out["replicated"] and out["dr_restore_count"]==1
Path("results/v36_governance_benchmark.json").write_text(json.dumps(out,indent=2))
