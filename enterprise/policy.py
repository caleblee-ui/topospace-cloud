
from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class Policy:
    max_context_tokens:int=64000
    max_agents:int=8
    allowed_tool_types:set=field(default_factory=set)
    deny_high_risk:bool=True
    max_risk:float=.75
    require_audit:bool=True

class PolicyEngine:
    def __init__(self):
        self.org_policies={}
        self.project_policies={}

    def set_org_policy(self,org_id,policy):
        self.org_policies[org_id]=policy

    def set_project_policy(self,org_id,project_id,policy):
        self.project_policies[(org_id,project_id)]=policy

    def effective(self,org_id,project_id=None):
        base=self.org_policies.get(org_id,Policy())
        if project_id is None or (org_id,project_id) not in self.project_policies:
            return base
        p=self.project_policies[(org_id,project_id)]
        return Policy(
            max_context_tokens=min(base.max_context_tokens,p.max_context_tokens),
            max_agents=min(base.max_agents,p.max_agents),
            allowed_tool_types=(base.allowed_tool_types & p.allowed_tool_types) if base.allowed_tool_types and p.allowed_tool_types else (p.allowed_tool_types or base.allowed_tool_types),
            deny_high_risk=base.deny_high_risk or p.deny_high_risk,
            max_risk=min(base.max_risk,p.max_risk),
            require_audit=base.require_audit or p.require_audit
        )

    def validate_context(self,policy,context,team):
        errors=[]
        total=sum(int(x.get("tokens",0)) for x in context)
        if total>policy.max_context_tokens: errors.append("context_token_policy")
        if len(team)>policy.max_agents: errors.append("agent_count_policy")
        if policy.deny_high_risk and any(float(x.get("risk",0))>policy.max_risk for x in team):
            errors.append("risk_policy")
        return {"ok":not errors,"errors":errors}
