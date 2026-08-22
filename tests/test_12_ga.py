from ga12.runtime import TopoSpaceGA
from ga12.provider_harness import LiveABHarness,ProviderUsage
from agent_gateway.contracts import GatewayRequest
def test_ga_e2e():
 d=TopoSpaceGA().optimize(GatewayRequest("x",[{"role":"user","content":"x"}],state={"risk":.4,"ambiguity":.4,"hierarchy":.4}));assert d.model and d.geometry_family and d.execution_path and d.api_version=="v1"
def test_usage_accounting():
 h=LiveABHarness();h.record("1","a",ProviderUsage(100,50,1,400,True,.1));assert h.compare()["a"]["mean_total_tokens"]==150
