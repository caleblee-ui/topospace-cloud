
from __future__ import annotations
from dataclasses import dataclass
from typing import Callable

@dataclass
class Migration:
    version:int
    name:str
    up:Callable

class MigrationRunner:
    def __init__(self,current_version=0):
        self.current_version=current_version
        self.migrations=[]

    def register(self,migration):
        self.migrations.append(migration)
        self.migrations.sort(key=lambda x:x.version)

    def migrate(self,target=None,context=None):
        applied=[]
        for m in self.migrations:
            if m.version<=self.current_version: continue
            if target is not None and m.version>target: break
            m.up(context)
            self.current_version=m.version
            applied.append({"version":m.version,"name":m.name})
        return applied
