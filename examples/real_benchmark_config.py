
"""Example wiring. Set provider key and replace context_builder/evaluator with your real task logic."""
from benchmarking.models import BenchmarkTask
from benchmarking.real_model_adapter import RealModelABAdapter
from benchmarking.paired_runner import PairedRealRunner
from providers.openai_compatible import OpenAIResponsesProvider
from evaluators.basic import ExactContainsEvaluator

def context_builder(task,mode):
    base="Analyze the following task and answer with PASS if the requested invariant holds.\nTask: "+task.prompt
    if mode=="baseline":
        prompt=base+"\nContext: full repository/context would be inserted here."
        return {"prompt":prompt,"tool_calls":6,"agent_invocations":3}
    prompt=base+"\nContext: TopoSpace-pruned relevant neighborhood would be inserted here."
    return {"prompt":prompt,"tool_calls":4,"agent_invocations":2}

if __name__=="__main__":
    provider=OpenAIResponsesProvider()
    adapter=RealModelABAdapter(provider,"PIN_MODEL_VERSION",context_builder,ExactContainsEvaluator(required=["PASS"]))
    tasks=[BenchmarkTask("real-1","Example invariant","coding")]
    print(PairedRealRunner(adapter,repeats=3).run(tasks))
