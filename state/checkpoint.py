
from __future__ import annotations
import sqlite3,json,threading,time

class CheckpointStore:
    def __init__(self,path="topospace_state.db"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.lock=threading.RLock()
        self.db.execute("""create table if not exists checkpoints(
          workspace_id text not null,
          run_id text not null,
          seq integer not null,
          payload text not null,
          created_at real not null,
          primary key(workspace_id,run_id,seq)
        )""")
        self.db.commit()

    def save(self,workspace_id,run_id,seq,payload):
        with self.lock:
            self.db.execute("insert or replace into checkpoints values(?,?,?,?,?)",
                            (workspace_id,run_id,int(seq),json.dumps(payload),time.time()))
            self.db.commit()

    def latest(self,workspace_id,run_id):
        with self.lock:
            row=self.db.execute("""select seq,payload,created_at from checkpoints
                where workspace_id=? and run_id=? order by seq desc limit 1""",(workspace_id,run_id)).fetchone()
        return None if not row else {"seq":row[0],"payload":json.loads(row[1]),"created_at":row[2]}
