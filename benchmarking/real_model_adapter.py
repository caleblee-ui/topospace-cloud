
from __future__ import annotations
from benchmarking.adapter import AgentBenchmarkAdapter
from benchmarking.models import RunRecord

class RealModelABAdapter(AgentBenchmarkAdapter):
    """Paired real-model benchmark adapter.

    context_builder(task, mode) -> dict(prompt, system?, tool_calls?, agent_invocations?, extra?)
    evaluator.evaluate(text, task) -> bool
    """
    def __init__(self,provider,model,context_builder,evaluator,price_fn=None,temperature=0.0,max_output_tokens=2048):
        self.provider=provider;self.model=model;self.context_builder=context_builder;self.evaluator=evaluator
        self.price_fn=price_fn;self.temperature=temperature;self.max_output_tokens=max_output_tokens

    def run(self,task,mode,run_index):
        ctx=self.context_builder(task,mode)
        res=self.provider.generate(model=self.model,prompt=ctx["prompt"],system=ctx.get("system",""),
                                   temperature=self.temperature,max_output_tokens=self.max_output_tokens)
        success=self.evaluator.evaluate(res.text,task)
        cost=res.usage.cost_usd
        if self.price_fn: cost=float(self.price_fn(res.usage,self.model))
        return RunRecord(task.id,mode,run_index,success,res.usage.input_tokens,res.usage.output_tokens,
          int(ctx.get("tool_calls",0)),int(ctx.get("agent_invocations",1)),res.latency_ms,cost,
          {"model":self.model,"cached_input_tokens":res.usage.cached_input_tokens,
           "provider":self.provider.__class__.__name__,"context_extra":ctx.get("extra",{})})
