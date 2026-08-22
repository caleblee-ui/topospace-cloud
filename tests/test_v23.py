
from pathlib import Path
import tempfile
from enterprise.rbac import RBAC,Principal
from enterprise.policy import PolicyEngine,Policy
from enterprise.audit import AuditLog
from enterprise.signed_config import SignedConfig
from enterprise.metrics import MetricsRegistry
from production.config import ProductionConfig

def test_rbac():
 r=RBAC();p=Principal("u",{"developer"},"o",{"p1"})
 assert r.authorize(p,"optimize","p1") and not r.authorize(p,"configure","p1") and not r.authorize(p,"optimize","p2")

def test_policy():
 e=PolicyEngine();e.set_org_policy("o",Policy(max_context_tokens=100,max_agents=2))
 p=e.effective("o");assert not e.validate_context(p,[{"tokens":120}],[])["ok"]

def test_audit_chain():
 with tempfile.TemporaryDirectory() as d:
  a=AuditLog(Path(d)/"a.db");a.append("u","x","r",{"a":1});a.append("u","y","r",{"b":2})
  assert a.verify() and len(a.list())==2

def test_signed_config():
 s=SignedConfig("secret");b=s.sign(ProductionConfig(),1);assert s.verify(b)
 b["payload"]["version"]=2;assert not s.verify(b)

def test_metrics():
 m=MetricsRegistry();m.inc("requests",labels={"org":"o"});m.set("workers",3)
 text=m.prometheus();assert 'requests{org="o"} 1.0' in text and "workers 3.0" in text
