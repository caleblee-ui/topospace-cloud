
from llm_runtime.contracts import LLMUsage,LLMRequest,LLMResult
from experiments.ab_runner import ABAgentExperiment
from observability12.metrics import RuntimeMetrics
from adapters.langchain import LangChainTopoSpaceAdapter

def test_ab_actual_usage_math():
    e=ABAgentExperiment()
    r=e.record("x",LLMUsage(1000,200,5,1000),LLMUsage(600,200,3,800),.9,.91)
    assert round(r["input_token_saving_pct"],1)==40.0
    assert r["quality_topospace"]>r["quality_baseline"]

def test_ab_summary():
    e=ABAgentExperiment()
    e.record("x",LLMUsage(100,10,2,100),LLMUsage(50,10,1,80),1,1)
    assert e.summary()["tasks"]==1

def test_metrics():
    m=RuntimeMetrics();m.observe("x",LLMUsage(10,2,1,30),"topospace")
    assert m.summary()["requests"]==1

def test_langchain_is_optional_thin_bridge():
    class M:
        def optimize(self,*args):return {"ok":True}
    a=LangChainTopoSpaceAdapter(M())
    assert a.preprocess(LLMRequest("x",[]),{})["ok"]
