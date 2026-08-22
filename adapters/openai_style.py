
from llm_runtime.contracts import LLMResult,LLMUsage
from llm_runtime.provider import LLMProvider

class OpenAIStyleAdapter(LLMProvider):
    """
    Adapter for clients exposing chat.completions.create(...).
    No vendor package is imported by TopoSpace.
    """
    def __init__(self,client): self.client=client

    def invoke(self,request,context=None,tools=None):
        messages=list(request.messages)
        if context:
            messages.append({"role":"system","content":"TopoSpace selected context: "+repr(context)})
        kwargs={"model":request.model,"messages":messages,"max_tokens":request.max_tokens}
        if tools: kwargs["tools"]=tools
        t=__import__("time").perf_counter()
        r=self.client.chat.completions.create(**kwargs)
        latency=(__import__("time").perf_counter()-t)*1000
        usage=getattr(r,"usage",None)
        inp=int(getattr(usage,"prompt_tokens",0) or 0)
        out=int(getattr(usage,"completion_tokens",0) or 0)
        text=r.choices[0].message.content or ""
        return LLMResult(text,LLMUsage(inp,out,0,latency,True),{"provider":"openai-style"})
