
from __future__ import annotations
import sqlite3, json
from pathlib import Path

class GraphStore:
    def __init__(self, path="topospace_graphs.db"):
        self.path=str(path)
        self.db=sqlite3.connect(self.path)
        self.db.execute("""create table if not exists graph_snapshots(
            workspace_id text not null,
            seq integer not null,
            payload text not null,
            created_at text default current_timestamp,
            primary key(workspace_id,seq)
        )""")
        self.db.commit()

    def save(self, workspace_id, seq, payload):
        self.db.execute("insert or replace into graph_snapshots(workspace_id,seq,payload) values(?,?,?)",
                        (workspace_id,int(seq),json.dumps(payload)))
        self.db.commit()

    def latest(self, workspace_id):
        row=self.db.execute("select seq,payload from graph_snapshots where workspace_id=? order by seq desc limit 1",
                            (workspace_id,)).fetchone()
        return None if not row else {"seq":row[0],"payload":json.loads(row[1])}

    def history(self, workspace_id, limit=100):
        rows=self.db.execute("select seq,payload,created_at from graph_snapshots where workspace_id=? order by seq desc limit ?",
                             (workspace_id,int(limit))).fetchall()
        return [{"seq":r[0],"payload":json.loads(r[1]),"created_at":r[2]} for r in rows]
