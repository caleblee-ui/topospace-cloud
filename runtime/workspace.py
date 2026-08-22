from dataclasses import dataclass, field
from core.state.space import TopoSpace
@dataclass
class Workspace:
    id:str; tenant_id:str; name:str; space:object=None; metadata:dict=field(default_factory=dict)
class WorkspaceRegistry:
    def __init__(self): self._items={}
    def create(self,tenant_id,workspace_id,name=None):
        key=(tenant_id,workspace_id)
        if key not in self._items:self._items[key]=Workspace(workspace_id,tenant_id,name or workspace_id)
        return self._items[key]
    def get(self,tenant_id,workspace_id):return self._items[(tenant_id,workspace_id)]
    def list(self,tenant_id=None):return [x for x in self._items.values() if tenant_id is None or x.tenant_id==tenant_id]
