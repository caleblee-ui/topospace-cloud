
import sqlite3,json,time,hashlib,threading

class AuditLog:
    """Append-only hash-chained audit log."""
    def __init__(self,path="topospace_audit.db"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.lock=threading.RLock()
        self.db.execute("""create table if not exists audit(
          seq integer primary key autoincrement,
          ts real not null,
          principal text not null,
          action text not null,
          resource text not null,
          payload text not null,
          prev_hash text not null,
          entry_hash text not null
        )""")
        self.db.commit()

    def _last_hash(self):
        row=self.db.execute("select entry_hash from audit order by seq desc limit 1").fetchone()
        return row[0] if row else ""

    def append(self,principal,action,resource,payload):
        with self.lock:
            ts=time.time();prev=self._last_hash();body=json.dumps(payload,sort_keys=True,separators=(",",":"))
            raw=f"{ts}|{principal}|{action}|{resource}|{body}|{prev}".encode()
            h=hashlib.sha256(raw).hexdigest()
            self.db.execute("insert into audit(ts,principal,action,resource,payload,prev_hash,entry_hash) values(?,?,?,?,?,?,?)",
                            (ts,principal,action,resource,body,prev,h));self.db.commit()
            return h

    def verify(self):
        rows=self.db.execute("select ts,principal,action,resource,payload,prev_hash,entry_hash from audit order by seq").fetchall()
        prev=""
        for ts,principal,action,resource,payload,prev_hash,entry_hash in rows:
            if prev_hash!=prev:return False
            raw=f"{ts}|{principal}|{action}|{resource}|{payload}|{prev_hash}".encode()
            if hashlib.sha256(raw).hexdigest()!=entry_hash:return False
            prev=entry_hash
        return True

    def list(self,limit=100):
        rows=self.db.execute("select seq,ts,principal,action,resource,payload,entry_hash from audit order by seq desc limit ?",(int(limit),)).fetchall()
        return [{"seq":r[0],"ts":r[1],"principal":r[2],"action":r[3],"resource":r[4],"payload":json.loads(r[5]),"hash":r[6]} for r in rows]
