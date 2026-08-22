
class PostgresCheckpointAdapter:
    """DB-API compatible PostgreSQL checkpoint adapter."""
    def __init__(self,connection):
        self.db=connection
    def init_schema(self):
        cur=self.db.cursor()
        cur.execute("""create table if not exists topospace_checkpoints(
          workspace_id text not null, run_id text not null, seq bigint not null,
          payload jsonb not null, created_at timestamptz default now(),
          primary key(workspace_id,run_id,seq))""")
        self.db.commit()
    def save(self,workspace_id,run_id,seq,payload_json):
        cur=self.db.cursor()
        cur.execute("""insert into topospace_checkpoints(workspace_id,run_id,seq,payload)
          values(%s,%s,%s,%s) on conflict(workspace_id,run_id,seq) do update set payload=excluded.payload""",
          (workspace_id,run_id,int(seq),payload_json))
        self.db.commit()
