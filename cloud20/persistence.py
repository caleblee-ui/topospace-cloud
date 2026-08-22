
import sqlite3,json,hashlib
class TenantRepository:
    """
    SQLite reference adapter. Production deployments can replace with PostgreSQL
    through the same method contract.
    """
    def __init__(self,path=":memory:"):
        self.db=sqlite3.connect(path,check_same_thread=False)
        self.db.execute("create table if not exists tenants(id text primary key, plan_json text)")
        self.db.execute("create table if not exists api_keys(key_hash text primary key, tenant_id text, active int)")
        self.db.commit()
    def put_tenant(self,tenant_id,plan):
        self.db.execute("insert or replace into tenants values(?,?)",(tenant_id,json.dumps(plan)));self.db.commit()
    def issue_key(self,tenant_id,raw_key):
        h=hashlib.sha256(raw_key.encode()).hexdigest()
        self.db.execute("insert or replace into api_keys values(?,?,1)",(h,tenant_id));self.db.commit()
    def auth(self,raw_key):
        h=hashlib.sha256(raw_key.encode()).hexdigest()
        r=self.db.execute("select tenant_id,active from api_keys where key_hash=?",(h,)).fetchone()
        if not r or not r[1]:raise PermissionError("invalid_api_key")
        return r[0]
