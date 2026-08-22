
from pathlib import Path
import tempfile,time
from governance.signing import PolicySigner
from governance.approval import ApprovalWorkflow
from governance.scheduler import RolloutScheduler
from governance.lineage import PolicyLineage
from replication.policy_replication import MultiRegionPolicyReplicator
from dr.policy_backup import PolicyDisasterRecovery
from policyops.tenant_isolation import TenantLearningIsolation

ROOT=Path(__file__).resolve().parents[1]

def test_signing():
 s=PolicySigner("x");x=s.sign("t","coding",1,{"a":1});assert s.verify(x["token"])["tenant_id"]=="t"

def test_approval():
 a=ApprovalWorkflow(2);a.create("r","t","x",1,"u")
 assert a.approve("r","a").status=="pending"
 assert a.approve("r","b").status=="approved"

def test_scheduler():
 s=RolloutScheduler();s.schedule(time.time()-1,"t","x",1,20);assert s.due()

def test_lineage():
 l=PolicyLineage();r=l.append("t","x",1,{"a":1});assert l.history("t","x")[0]["content_hash"]==r["content_hash"]

def test_replication():
 r=MultiRegionPolicyReplicator(["a","b"]);r.replicate("k",{"x":1});assert r.verify("k")

def test_dr_bundle():
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/"b.json";m=PolicyDisasterRecovery();m.export_bundle(p,[{"a":1}],[])
  assert m.restore_bundle(p)["policies"][0]["a"]==1

def test_tenant_learning_isolation():
 class L: pass
 x=TenantLearningIsolation(L)
 assert x.get("a") is not x.get("b")
 assert x.get("a") is x.get("a")

def test_governance_visual():
 assert "customElements.define" in (ROOT/"web-sdk/governance-panel.js").read_text()
