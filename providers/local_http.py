
from __future__ import annotations
import json,time,urllib.request
from providers.base import ModelProvider,ModelResult,ModelUsage
class LocalHTTPProvider(ModelProvider):
    """Generic local endpoint. Expected JSON response: text, usage.input_tokens/output_tokens."""
    def __init__(self,url):self.url=url
    def generate(self,*,model,prompt,system="",temperature=0.0,max_output_tokens=2048,**kwargs):
        payload={"model":model,"prompt":prompt,"system":system,"temperature":temperature,"max_output_tokens":max_output_tokens}
        start=time.perf_counter()
        req=urllib.request.Request(self.url,data=json.dumps(payload).encode(),headers={"content-type":"application/json"},method="POST")
        with urllib.request.urlopen(req,timeout=kwargs.get("timeout",120)) as r:obj=json.loads(r.read())
        u=obj.get("usage") or {};lat=(time.perf_counter()-start)*1000
        return ModelResult(obj.get("text",""),ModelUsage(int(u.get("input_tokens",0)),int(u.get("output_tokens",0)),int(u.get("cached_input_tokens",0)),float(u.get("cost_usd",0))),lat,obj)
