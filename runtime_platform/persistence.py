
import json,sqlite3,threading,time
class EventStore:
 def __init__(self,path=":memory:"):
  self.db=sqlite3.connect(path,check_same_thread=False);self.lock=threading.Lock()
  self.db.execute("create table if not exists events(id integer primary key,tenant text,task text,hook text,payload text,ts real)")
  self.db.execute("create table if not exists policies(tenant text,name text,value text,primary key(tenant,name))");self.db.commit()
 def append(self,t,task,h,p):
  with self.lock:self.db.execute("insert into events(tenant,task,hook,payload,ts) values(?,?,?,?,?)",(t,task,h,json.dumps(p),time.time()));self.db.commit()
 def count(self,t):return self.db.execute("select count(*) from events where tenant=?",(t,)).fetchone()[0]
 def events(self,t,limit=100):return [{"task":r[0],"hook":r[1],"payload":json.loads(r[2])} for r in self.db.execute("select task,hook,payload from events where tenant=? order by id desc limit ?",(t,limit))]
 def set_policy(self,t,n,v):
  with self.lock:self.db.execute("insert or replace into policies values(?,?,?)",(t,n,json.dumps(v)));self.db.commit()
 def policy(self,t,n,default=None):
  r=self.db.execute("select value from policies where tenant=? and name=?",(t,n)).fetchone();return json.loads(r[0]) if r else default
