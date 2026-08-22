
from llm_runtime.contracts import LLMResult,LLMUsage
from llm_runtime.provider import LLMProvider

class AnthropicStyleAdapter(LLMProvider):
    """Adapter for clients exposing messages.create(...)."""
    def __init__(self,client): self.client=client
    def invoke(self,request,context=None,tools=None):
        system="TopoSpace selected context: "+repr(context or [])
        kwargs={"model":request.model,"messages":request.messages,"max_tokens":request.max_tokens,"system":system}
        if tools: kwargs["tools"]=tools
        t=__import__("time").perf_counter()
        r=self.client.messages.create(**kwargs)
        latency=(__import__("time").perf_counter()-t)*1000
        usage=getattr(r,"usage",None)
        inp=int(getattr(usage,"input_tokens",0) or 0)
        out=int(getattr(usage,"output_tokens",0) or 0)
        text="".join(getattr(x,"text","") for x in getattr(r,"content",[]))
        return LLMResult(text,LLMUsage(inp,out,0,latency,True),{"provider":"anthropic-style"})
