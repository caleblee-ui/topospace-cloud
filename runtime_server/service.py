
from runtime_sdk.middleware import TopoSpaceMiddleware
from runtime_sdk.adapter import AgentRuntimeAdapter
from runtime_server.tenant import TenantScope

class RuntimeService:
    def __init__(self):
        self.tenants={}
    def _middleware(self,tenant_id):
        if tenant_id not in self.tenants:self.tenants[tenant_id]=TopoSpaceMiddleware()
        return self.tenants[tenant_id]
    def adapter(self,scope:TenantScope):
        return AgentRuntimeAdapter(self._middleware(scope.tenant_id),scope.agent_id)
    def dispatch(self,scope,hook,task_id,payload=None):
        payload=payload or {}
        a=self.adapter(scope)
        fn=getattr(a,hook)
        return fn(task_id,**payload)
    def snapshot(self,tenant_id):
        return self._middleware(tenant_id).snapshot()
