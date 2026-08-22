
from cloud19.service import TopoSpaceCloudService
class ExecutingTopoSpaceCloudService(TopoSpaceCloudService):
    def __init__(self,*args,provider_router=None,billing=None,default_provider="primary",**kwargs):
        super().__init__(*args,**kwargs)
        self.provider_router=provider_router;self.billing=billing;self.default_provider=default_provider

    def execute_chat(self,api_key,request,state=None):
        plan=self.chat_completions(api_key,request,state)
        if self.provider_router is None:return plan
        auth=self.keys.authenticate(api_key);tenant=auth["tenant_id"]
        topo=plan["topospace"];model=plan["model"]
        response=self.provider_router.complete(self.default_provider,model,request.messages,topo["token_budget"],request.metadata)
        self.meter.record(tenant,model,response.input_tokens,response.output_tokens,response.cost,response.latency_ms,True)
        if self.billing:self.billing.record(tenant,plan["id"],response.metadata.get("provider",""),model,response.cost,response.input_tokens,response.output_tokens)
        return {"id":plan["id"],"object":"chat.completion","model":model,
                "choices":[{"index":0,"message":{"role":"assistant","content":response.text},"finish_reason":"stop"}],
                "usage":{"prompt_tokens":response.input_tokens,"completion_tokens":response.output_tokens,
                         "total_tokens":response.input_tokens+response.output_tokens},
                "topospace":topo,"provider":response.metadata.get("provider")}

    def stream_chat(self,api_key,request,state=None):
        plan=self.chat_completions(api_key,request,state)
        if self.provider_router is None:
            yield {"event":"plan","data":plan};return
        # streaming uses selected provider directly; production adapter may implement streaming failover semantics.
        p=self.provider_router.providers[self.default_provider]
        for event in p.stream(plan["model"],request.messages,plan["topospace"]["token_budget"],request.metadata):
            yield {"event":event["type"],"data":event}
