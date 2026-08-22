
from providers.base import ModelProvider,ModelResult,ModelUsage
from benchmarking.real_model_adapter import RealModelABAdapter
from benchmarking.models import BenchmarkTask
from evaluators.basic import ExactContainsEvaluator

class FakeProvider(ModelProvider):
    def generate(self,**kwargs):
        p=kwargs["prompt"]
        inp=1000 if "full" in p else 600
        return ModelResult("PASS",ModelUsage(inp,100,0,.01),50,{})

def test_real_model_adapter_usage():
    def ctx(task,mode):
        return {"prompt":"full" if mode=="baseline" else "pruned","tool_calls":3 if mode=="baseline" else 2,"agent_invocations":2 if mode=="baseline" else 1}
    a=RealModelABAdapter(FakeProvider(),"x",ctx,ExactContainsEvaluator(["PASS"]))
    b=a.run(BenchmarkTask("t","q","coding"),"baseline",0)
    o=a.run(BenchmarkTask("t","q","coding"),"topospace",0)
    assert b.input_tokens==1000 and o.input_tokens==600 and b.success and o.success

def test_exact_evaluator():
    assert ExactContainsEvaluator(["ok"],["bad"]).evaluate("OK good")
