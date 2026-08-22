
from cloud19.auth import APIKeyStore
from cloud19.rate_limit import SlidingWindowRateLimiter
from cloud19.metering import UsageMeter
from cloud19.tenant import TenantPlan
from cloud19.openai_compat import ChatCompletionRequest
from cloud20.fake_provider import DeterministicProvider
from cloud20.resilience import ResilientProviderRouter
from cloud20.billing import BillingLedger
from cloud20.service import ExecutingTopoSpaceCloudService
from cloud20.persistence import TenantRepository

def setup():
    k=APIKeyStore();k.issue("t1","sk-test");plans={"t1":TenantPlan("t1",100,100000,100)}
    p1=DeterministicProvider("p1");p2=DeterministicProvider("p2")
    router=ResilientProviderRouter({"primary":p1,"fallback":p2},retries=0)
    bill=BillingLedger()
    s=ExecutingTopoSpaceCloudService(k,SlidingWindowRateLimiter(),UsageMeter(),plans,provider_router=router,billing=bill)
    return s,p1,p2,bill

def test_real_execution_path():
    s,_,_,b=setup()
    out=s.execute_chat("sk-test",ChatCompletionRequest([{"role":"user","content":"hello"}]),{"risk":.2})
    assert out["object"]=="chat.completion" and out["choices"][0]["message"]["content"]
    assert b.invoice_summary("t1")["requests"]==1

def test_provider_fallback():
    s,p1,p2,_=setup();p1.fail=True
    out=s.execute_chat("sk-test",ChatCompletionRequest([{"role":"user","content":"hello"}]))
    assert out["provider"]=="fallback"

def test_stream_events():
    s,_,_,_=setup()
    ev=list(s.stream_chat("sk-test",ChatCompletionRequest([{"role":"user","content":"x"}])))
    assert ev[0]["event"]=="message_start" and ev[-1]["event"]=="message_end"

def test_persistent_tenant_repo(tmp_path):
    r=TenantRepository(str(tmp_path/"t.db"));r.put_tenant("x",{"rpm":10});r.issue_key("x","sk-x")
    assert r.auth("sk-x")=="x"
