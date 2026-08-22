
from __future__ import annotations
import os,json,time,urllib.request
from providers.base import ModelProvider,ModelResult,ModelUsage

class OpenAIResponsesProvider(ModelProvider):
    """Minimal OpenAI Responses API adapter using only stdlib HTTP.

    Expected response usage fields: input_tokens, output_tokens, total_tokens.
    """
    def __init__(self,api_key=None,base_url="https://api.openai.com/v1"):
        self.api_key=api_key or os.getenv("OPENAI_API_KEY")
        self.base_url=base_url.rstrip("/")

    def generate(self,*,model,prompt,system="",temperature=0.0,max_output_tokens=2048,**kwargs):
        if not self.api_key: raise RuntimeError("OPENAI_API_KEY is required")
        body={"model":model,"input":([{"role":"system","content":system}] if system else [])+[{"role":"user","content":prompt}],
              "max_output_tokens":max_output_tokens}
        if temperature is not None: body["temperature"]=temperature
        req=urllib.request.Request(self.base_url+"/responses",data=json.dumps(body).encode(),
          headers={"Authorization":"Bearer "+self.api_key,"Content-Type":"application/json"},method="POST")
        start=time.perf_counter()
        with urllib.request.urlopen(req,timeout=kwargs.get("timeout",120)) as r: obj=json.loads(r.read())
        latency=(time.perf_counter()-start)*1000
        usage=obj.get("usage") or {}
        text=obj.get("output_text")
        if text is None:
            pieces=[]
            for item in obj.get("output",[]):
                for c in item.get("content",[]) if isinstance(item,dict) else []:
                    if isinstance(c,dict) and c.get("text"):pieces.append(c["text"])
            text="\n".join(pieces)
        cached=((usage.get("input_tokens_details") or {}).get("cached_tokens",0))
        return ModelResult(text or "",ModelUsage(int(usage.get("input_tokens",0)),int(usage.get("output_tokens",0)),int(cached),0.0),latency,obj)
