
import json,time,urllib.request,urllib.error
from cloud20.provider import ProviderAdapter,ProviderResponse

class OpenAICompatibleHTTPProvider(ProviderAdapter):
    """
    Generic provider for OpenAI-compatible /chat/completions HTTP APIs.
    Compatible endpoints can include OpenAI-style gateways and local model servers.
    """
    def __init__(self,base_url,api_key,timeout=60,provider_name="openai-compatible"):
        self.base_url=base_url.rstrip("/")
        self.api_key=api_key
        self.timeout=timeout
        self.provider_name=provider_name

    def complete(self,model,messages,max_tokens,metadata=None):
        payload={"model":model,"messages":messages,"max_tokens":int(max_tokens),"stream":False}
        req=urllib.request.Request(
            self.base_url+"/chat/completions",
            data=json.dumps(payload).encode(),
            method="POST",
            headers={"content-type":"application/json","authorization":"Bearer "+self.api_key}
        )
        t=time.perf_counter()
        try:
            with urllib.request.urlopen(req,timeout=self.timeout) as r:
                data=json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"provider_http_{e.code}") from e
        latency=(time.perf_counter()-t)*1000
        usage=data.get("usage",{})
        choices=data.get("choices",[])
        text=""
        if choices:
            text=(choices[0].get("message") or {}).get("content","") or ""
        return ProviderResponse(
            text=text,model=data.get("model",model),
            input_tokens=int(usage.get("prompt_tokens",usage.get("input_tokens",0)) or 0),
            output_tokens=int(usage.get("completion_tokens",usage.get("output_tokens",0)) or 0),
            tool_calls=0,latency_ms=latency,cost=0.0,
            metadata={"provider":self.provider_name,"raw_id":data.get("id")}
        )
