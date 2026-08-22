
from production.engine import TopoSpaceEngine
from production.config import ProductionConfig
from production.guardrails import RuntimeGuardrails

def fixture():
 c=[{"id":"a","tokens":100,"utility":1,"distance":.1,"score":.9,"drift":.1},
    {"id":"b","tokens":100,"utility":.1,"distance":.8,"score":.1,"drift":.8}]
 a=[{"id":"code","capabilities":["code"],"score":.9,"reliability":1,"cost":.1,"risk":.05}]
 return c,a

def test_engine_optimizes_and_caches():
 c,a=fixture();e=TopoSpaceEngine(ProductionConfig(max_context_tokens=500,reserve_output_tokens=100))
 r=e.optimize("x",c,a,["code"]);r2=e.optimize("x",c,a,["code"])
 assert [x["id"] for x in r["context"]]==["a"]
 assert r2["cache_hit"] is True

def test_guardrails():
 assert not RuntimeGuardrails(max_agents=2).validate(agents=3)["ok"]

def test_fail_open():
 c,a=fixture();e=TopoSpaceEngine()
 e.pruner.prune=lambda *args,**kwargs: (_ for _ in ()).throw(RuntimeError("boom"))
 r=e.optimize("x",c,a,["code"])
 assert "optimizer_fail_open" in r["guardrails"]["errors"]
