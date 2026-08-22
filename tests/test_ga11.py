
from pathlib import Path
from ga.version import VERSION,STATUS
from ga11.readiness import GAReadiness
from online_learning.rollout import StagedRolloutManager
from online_learning.rollback import JointAutomaticRollback
ROOT=Path(__file__).resolve().parents[1]

def test_version_ga():
    assert VERSION.startswith("1.3.") and STATUS in {"ALPHA","BETA","GA"}

def test_readiness():
    assert GAReadiness(ROOT).checks()["ok"]

def test_rollout_stages():
    r=StagedRolloutManager()
    assert [r.start(),r.advance(),r.advance(),r.advance()]==[5,25,50,100]

def test_rollback_guard():
    rb=JointAutomaticRollback()
    assert rb.check({"reward":.8,"latency_ms":10},{"reward":.7,"latency_ms":13})["rollback"]
