
from pathlib import Path
from runtime_server.service import RuntimeService
from runtime_server.tenant import TenantScope
from runtime_server.auth import APIKeyAuth
from runtime_sdk.adapters.custom import CustomAgentAdapter
ROOT=Path(__file__).resolve().parents[1]

def test_tenant_isolation():
 s=RuntimeService()
 a=TenantScope("a",agent_id="x");b=TenantScope("b",agent_id="x")
 s.dispatch(a,"task_start","t",{})
 assert "t" in s.snapshot("a")["tasks"] and "t" not in s.snapshot("b")["tasks"]

def test_api_key_auth():
 a=APIKeyAuth({"k":"s"});assert a.verify("k","s") and not a.verify("k","bad")

def test_service_lifecycle():
 s=RuntimeService();scope=TenantScope("t",agent_id="a")
 assert s.dispatch(scope,"task_start","task",{})[0]["status"]=="started"
 s.dispatch(scope,"task_complete","task",{"success":True})
 assert s.snapshot("t")["tasks"]["task"]["success"] is True

def test_adapter_contract():
 class C:
  def task_start(self,*a,**k):return 1
 c=CustomAgentAdapter(C());assert c.task_start("x")==1

def test_beta_assets():
 assert (ROOT/"deploy/beta/Dockerfile").exists()
 assert "customElements.define" in (ROOT/"web-sdk/beta-runtime-panel.js").read_text()
