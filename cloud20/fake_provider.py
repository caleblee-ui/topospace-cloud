
import time
from cloud20.provider import ProviderAdapter,ProviderResponse
class DeterministicProvider(ProviderAdapter):
    def __init__(self,name="mock"):self.name=name;self.fail=False
    def complete(self,model,messages,max_tokens,metadata=None):
        if self.fail:raise RuntimeError("provider_failure")
        t=time.perf_counter()
        prompt=" ".join(x.get("content","") for x in messages)
        text=f"[{model}] "+prompt[:max(1,min(len(prompt),max_tokens))]
        latency=(time.perf_counter()-t)*1000
        return ProviderResponse(text,model,max(1,len(prompt)//4),max(1,len(text)//4),0,latency,.001)
