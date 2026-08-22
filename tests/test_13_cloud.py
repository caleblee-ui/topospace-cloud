
from cloud19.auth import APIKeyStore
from cloud19.rate_limit import SlidingWindowRateLimiter
from cloud19.metering import UsageMeter
from cloud19.tenant import TenantPlan
from cloud19.openai_compat import ChatCompletionRequest
from cloud19.service import TopoSpaceCloudService

def setup(limit=60):
    k=APIKeyStore();k.issue("t1","sk-test");p={"t1":TenantPlan("t1",limit,10000,10)}
    return TopoSpaceCloudService(k,SlidingWindowRateLimiter(),UsageMeter(),p)

def test_cloud_plan():
    s=setup();o=s.chat_completions("sk-test",ChatCompletionRequest([{"role":"user","content":"hello"}]),{"risk":.2})
    assert o["object"]=="chat.completion.plan" and o["model"]

def test_bad_key():
    s=setup()
    try:s.chat_completions("bad",ChatCompletionRequest([]));assert False
    except PermissionError:pass

def test_rate_limit():
    s=setup(1);q=ChatCompletionRequest([])
    s.chat_completions("sk-test",q)
    try:s.chat_completions("sk-test",q);assert False
    except RuntimeError as e:assert str(e)=="rate_limit_exceeded"

def test_meter_quota():
    s=setup();s.meter.record("t1","fast",5000,6000,1,10,True)
    try:s.chat_completions("sk-test",ChatCompletionRequest([]));assert False
    except RuntimeError as e:assert str(e)=="quota_exceeded"
