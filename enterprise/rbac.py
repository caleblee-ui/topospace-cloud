
from dataclasses import dataclass, field
from typing import Dict, Set

DEFAULT_ROLES={
    "viewer":{"read"},
    "developer":{"read","optimize"},
    "operator":{"read","optimize","configure","deploy"},
    "admin":{"read","optimize","configure","deploy","manage_users","read_audit"},
}

@dataclass
class Principal:
    id:str
    roles:Set[str]=field(default_factory=set)
    org_id:str="default"
    project_ids:Set[str]=field(default_factory=set)

class RBAC:
    def __init__(self,roles=None):
        self.roles=roles or DEFAULT_ROLES

    def permissions(self,principal):
        out=set()
        for role in principal.roles:
            out.update(self.roles.get(role,set()))
        return out

    def authorize(self,principal,permission,project_id=None):
        if permission not in self.permissions(principal):
            return False
        if project_id and principal.project_ids and project_id not in principal.project_ids:
            return False
        return True
