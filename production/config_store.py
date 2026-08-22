
from __future__ import annotations
import sqlite3,json,threading
from dataclasses import asdict
from production.config import ProductionConfig

class ConfigStore:
    def __init__(self,path="topospace_config.db"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.lock=threading.RLock()
        self.db.execute("""create table if not exists configs(
          workspace_id text primary key,
          version integer not null,
          payload text not null,
          updated_at text default current_timestamp
        )""")
        self.db.commit()

    def get(self,workspace_id):
        with self.lock:
            row=self.db.execute("select version,payload from configs where workspace_id=?",(workspace_id,)).fetchone()
        if not row:return {"version":0,"config":ProductionConfig()}
        return {"version":row[0],"config":ProductionConfig(**json.loads(row[1]))}

    def put(self,workspace_id,config,expected_version=None):
        with self.lock:
            current=self.get(workspace_id)
            if expected_version is not None and current["version"]!=expected_version:
                raise RuntimeError("config_version_conflict")
            version=current["version"]+1
            self.db.execute("insert or replace into configs(workspace_id,version,payload) values(?,?,?)",
                            (workspace_id,version,json.dumps(asdict(config))))
            self.db.commit()
        return version
