
from pathlib import Path
import tempfile
from policyops.store import PolicyStore
from policyops.champion import ChampionChallenger,PolicyCandidate
from policyops.rollback import AutomaticRollback
from policyops.drift import ConceptDriftDetector
from policyops.explain import PolicyExplainer

ROOT=Path(__file__).resolve().parents[1]

def test_policy_store():
 with tempfile.TemporaryDirectory() as d:
  s=PolicyStore(Path(d)/"p.db");v=s.save("t","coding",{"x":1},"champion")
  assert v==1 and s.latest("t","coding","champion")["payload"]["x"]==1

def test_champion_challenger():
 c=PolicyCandidate("c",1,.4,.95,.1,100);x=PolicyCandidate("x",2,.45,.945,.1,100)
 assert ChampionChallenger().evaluate(c,x)["promote"]

def test_rollback():
 assert AutomaticRollback().check({"success_rate":.95,"p95_ms":100},{"success_rate":.80,"p95_ms":100})["rollback"]

def test_drift():
 d=ConceptDriftDetector(threshold=.05)
 assert d.detect([.1]*100,[.9]*100)["drift"]

def test_explainer():
 x=PolicyExplainer().explain({"epsilon":.4},{"uncertainty":.8})
 assert "uncertainty" in x["summary"].lower()

def test_policyops_visual():
 assert "customElements.define" in (ROOT/"web-sdk/policyops-panel.js").read_text()
