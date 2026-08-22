
from dataclasses import dataclass
@dataclass(frozen=True)
class TenantScope:
    tenant_id:str
    project_id:str="default"
    agent_id:str="agent"
