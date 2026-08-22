
from agent_gateway.context import ContextBudgeter
from agent_gateway.model_router import ModelRouter
from agent_gateway.cache import SemanticDecisionCache
from agent_gateway.contracts import GatewayRequest
from agent_gateway.compat import OpenAICompatibleGateway

def test_budget_contracts_under_pressure():
    b=ContextBudgeter()
    assert b.budget(1000,1,1)<b.budget(1000,0,0)

def test_model_router():
    r=ModelRouter()
    assert r.route("auto",{"risk":.9})=="reasoning"
    assert r.route("auto",{"latency_pressure":.9})=="fast"
    assert r.route("fixed",{})=="fixed"

def test_cache_key_stable():
    c=SemanticDecisionCache()
    r=GatewayRequest("x",[{"role":"user","content":"a"}])
    assert c.key(r)==c.key(r)

def test_openai_compat_builds_request():
    class G:
        def optimize(self,r): return r
    x=OpenAICompatibleGateway(G()).optimize_payload({"model":"auto","messages":[]},{"memory":[]},{"risk":.1})
    assert x.model=="auto" and x.state["risk"]==.1
