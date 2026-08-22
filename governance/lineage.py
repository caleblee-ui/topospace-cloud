
from __future__ import annotations
import hashlib,json,time,threading

class PolicyLineage:
    """Append-only policy lineage with content hashes and parent links."""
    def __init__(self):
        self.rows=[];self.lock=threading.RLock()

    def append(self,tenant_id,task_type,version,payload,parent_hash=None,actor="system",action="created"):
        body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        content_hash=hashlib.sha256(body).hexdigest()
        row={
          "tenant_id":tenant_id,"task_type":task_type,"version":int(version),
          "content_hash":content_hash,"parent_hash":parent_hash,
          "actor":actor,"action":action,"ts":time.time()
        }
        with self.lock:self.rows.append(row)
        return row

    def history(self,tenant_id,task_type):
        with self.lock:
            return [x for x in self.rows if x["tenant_id"]==tenant_id and x["task_type"]==task_type]
