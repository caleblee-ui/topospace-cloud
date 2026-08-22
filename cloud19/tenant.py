
from dataclasses import dataclass
@dataclass
class TenantPlan:
    tenant_id:str
    requests_per_minute:int=60
    monthly_token_limit:int=1_000_000
    monthly_cost_limit:float=100.0
