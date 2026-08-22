from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Iterable, Optional
from core.objects import TopoObject


class SQLiteObjectStore:
    """Small production-oriented persistent store for TopoObject + trace JSON.

    It is intentionally dependency-free. ANN candidate generation is a separate
    interface so this store can later be replaced by pgvector/Qdrant/etc.
    """
    def __init__(self, path="topospace.db"):
        self.path = str(path)
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.execute("PRAGMA journal_mode=WAL")
        self.conn.execute("PRAGMA synchronous=NORMAL")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS objects (
            id TEXT PRIMARY KEY, type TEXT NOT NULL, features TEXT NOT NULL,
            metadata TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP)""")
        self.conn.execute("""CREATE TABLE IF NOT EXISTS traces (
            sequence INTEGER, session_id TEXT, payload TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY(session_id, sequence))""")
        self.conn.commit()

    def upsert(self, obj: TopoObject):
        self.conn.execute("""INSERT INTO objects(id,type,features,metadata)
          VALUES(?,?,?,?) ON CONFLICT(id) DO UPDATE SET type=excluded.type,
          features=excluded.features, metadata=excluded.metadata,
          updated_at=CURRENT_TIMESTAMP""",
          (obj.id, obj.type, json.dumps(obj.features), json.dumps(obj.metadata)))
        self.conn.commit(); return obj

    def get(self, object_id: str) -> Optional[TopoObject]:
        row = self.conn.execute("SELECT id,type,features,metadata FROM objects WHERE id=?", (object_id,)).fetchone()
        return None if not row else TopoObject(row[0], row[1], json.loads(row[2]), json.loads(row[3]))

    def objects(self, type: Optional[str]=None) -> Iterable[TopoObject]:
        sql="SELECT id,type,features,metadata FROM objects"; args=()
        if type is not None: sql += " WHERE type=?"; args=(type,)
        return [TopoObject(r[0],r[1],json.loads(r[2]),json.loads(r[3])) for r in self.conn.execute(sql,args)]

    def save_trace(self, session_id: str, sequence: int, payload: dict):
        self.conn.execute("INSERT OR REPLACE INTO traces(sequence,session_id,payload) VALUES(?,?,?)",
                          (sequence, session_id, json.dumps(payload)))
        self.conn.commit()

    def traces(self, session_id: str):
        rows=self.conn.execute("SELECT payload FROM traces WHERE session_id=? ORDER BY sequence",(session_id,)).fetchall()
        return [json.loads(r[0]) for r in rows]

    def close(self): self.conn.close()
