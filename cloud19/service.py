
import uuid,time
from ga12.runtime import TopoSpaceGA
from cloud19.openai_compat import to_gateway
class TopoSpaceCloudService:
    def __init__(self,key_store,rate_limiter,meter,plans):
        self.ga=TopoSpaceGA();self.keys=key_store;self.rate=rate_limiter;self.meter=meter;self.plans=plans
    def chat_completions(self,api_key,request,state=None):
        auth=self.keys.authenticate(api_key);tid=auth["tenant_id"];plan=self.plans[tid]
        if not self.rate.allow(tid,plan.requests_per_minute):raise RuntimeError("rate_limit_exceeded")
        if not self.meter.quota_ok(plan):raise RuntimeError("quota_exceeded")
        task_id="chatcmpl-"+uuid.uuid4().hex
        d=self.ga.optimize(to_gateway(task_id,request,state))
        # Provider invocation is deliberately adapter-owned; this layer returns the optimized execution plan.
        return {"id":task_id,"object":"chat.completion.plan","model":d.model,
                "topospace":{"geometry":d.geometry_family,"execution_path":d.execution_path,
                             "token_budget":d.token_budget,"api_version":d.api_version}}
