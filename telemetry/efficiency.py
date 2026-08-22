
from dataclasses import dataclass,asdict

@dataclass
class RunMetrics:
    input_tokens:int=0
    output_tokens:int=0
    tool_calls:int=0
    agent_invocations:int=0
    latency_ms:float=0
    cost_usd:float=0
    success:bool=False

def reduction(base,opt,field):
    b=float(getattr(base,field));o=float(getattr(opt,field))
    return 0.0 if b<=0 else 100.0*(1.0-o/b)

def compare(base:RunMetrics,opt:RunMetrics):
    return {
      "token_reduction_pct":reduction(base,opt,"input_tokens") if base.output_tokens==opt.output_tokens==0 else
        100*(1-(opt.input_tokens+opt.output_tokens)/max(1,base.input_tokens+base.output_tokens)),
      "input_token_reduction_pct":reduction(base,opt,"input_tokens"),
      "tool_call_reduction_pct":reduction(base,opt,"tool_calls"),
      "agent_invocation_reduction_pct":reduction(base,opt,"agent_invocations"),
      "latency_reduction_pct":reduction(base,opt,"latency_ms"),
      "cost_reduction_pct":reduction(base,opt,"cost_usd"),
      "success_delta_pp":100*(int(opt.success)-int(base.success)),
      "baseline":asdict(base),"optimized":asdict(opt)
    }
