
from __future__ import annotations
import os,json,time,urllib.request
from providers.base import ModelProvider,ModelResult,ModelUsage

class AnthropicMessagesProvider(ModelProvider):
    def __init__(self,api_key=None,base_url="https://api.anthropic.com/v1",version="2023-06-01"):
        self.api_key=api_key or os.getenv("ANTHROPIC_API_KEY");self.base_url=base_url.rstrip("/");self.version=version

    def generate(self,*,model,prompt,system="",temperature=0.0,max_output_tokens=2048,**kwargs):
        if not self.api_key:raise RuntimeError("ANTHROPIC_API_KEY is required")
        body={"model":model,"messages":[{"role":"user","content":prompt}],"max_tokens":max_output_tokens,"temperature":temperature}
        if system:body["system"]=system
        req=urllib.request.Request(self.base_url+"/messages",data=json.dumps(body).encode(),
          headers={"x-api-key":self.api_key,"anthropic-version":self.version,"content-type":"application/json"},method="POST")
        start=time.perf_counter()
        with urllib.request.urlopen(req,timeout=kwargs.get("timeout",120)) as r:obj=json.loads(r.read())
        latency=(time.perf_counter()-start)*1000
        usage=obj.get("usage") or {};text="\n".join(x.get("text","") for x in obj.get("content",[]) if x.get("type")=="text")
        return ModelResult(text,ModelUsage(int(usage.get("input_tokens",0)),int(usage.get("output_tokens",0)),0,0.0),latency,obj)
