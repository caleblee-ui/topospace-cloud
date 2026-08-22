
import sqlite3,json,time,threading

class PersistentCache:
    def __init__(self,path="topospace_cache.db"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.lock=threading.RLock()
        self.db.execute("""create table if not exists cache(
          k text primary key,
          payload text not null,
          expires_at real
        )""")
        self.db.commit()

    def get(self,key):
        with self.lock:
            row=self.db.execute("select payload,expires_at from cache where k=?",(key,)).fetchone()
            if not row:return None
            if row[1] is not None and row[1] < time.time():
                self.db.execute("delete from cache where k=?",(key,));self.db.commit();return None
            return json.loads(row[0])

    def put(self,key,value,ttl=None):
        exp=None if ttl is None else time.time()+ttl
        with self.lock:
            self.db.execute("insert or replace into cache(k,payload,expires_at) values(?,?,?)",(key,json.dumps(value),exp));self.db.commit()

    def delete(self,key):
        with self.lock:self.db.execute("delete from cache where k=?",(key,));self.db.commit()
