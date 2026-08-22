
from __future__ import annotations
import sqlite3,json,threading,time

class PolicyStore:
    def __init__(self,path="topospace_policies.db"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.lock=threading.RLock()
        self.db.execute("""create table if not exists policies(
          tenant_id text not null,
          task_type text not null,
          version integer not null,
          payload text not null,
          status text not null,
          created_at real not null,
          primary key(tenant_id,task_type,version)
        )""")
        self.db.commit()

    def save(self,tenant_id,task_type,payload,status="candidate"):
        with self.lock:
            row=self.db.execute("select max(version) from policies where tenant_id=? and task_type=?",
                                (tenant_id,task_type)).fetchone()
            version=(row[0] or 0)+1
            self.db.execute("insert into policies values(?,?,?,?,?,?)",
                            (tenant_id,task_type,version,json.dumps(payload),status,time.time()))
            self.db.commit()
        return version

    def latest(self,tenant_id,task_type,status=None):
        sql="select version,payload,status,created_at from policies where tenant_id=? and task_type=?"
        args=[tenant_id,task_type]
        if status:
            sql+=" and status=?";args.append(status)
        sql+=" order by version desc limit 1"
        row=self.db.execute(sql,tuple(args)).fetchone()
        return None if not row else {"version":row[0],"payload":json.loads(row[1]),"status":row[2],"created_at":row[3]}

    def set_status(self,tenant_id,task_type,version,status):
        with self.lock:
            self.db.execute("update policies set status=? where tenant_id=? and task_type=? and version=?",
                            (status,tenant_id,task_type,int(version)))
            self.db.commit()
