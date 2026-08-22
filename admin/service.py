
from __future__ import annotations
from customer.metering import UsageMeter

class AdminService:
    def __init__(self,meter=None):
        self.meter=meter or UsageMeter()
        self.tenants={}

    def create_tenant(self,tenant_id,plan="standard"):
        if tenant_id in self.tenants: raise ValueError("tenant_exists")
        self.tenants[tenant_id]={"id":tenant_id,"plan":plan,"enabled":True}
        return self.tenants[tenant_id]

    def disable_tenant(self,tenant_id):
        if tenant_id not in self.tenants: raise KeyError(tenant_id)
        self.tenants[tenant_id]["enabled"]=False
        return self.tenants[tenant_id]

    def usage(self,tenant_id):
        return self.meter.snapshot(tenant_id)
