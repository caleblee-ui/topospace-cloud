
from __future__ import annotations
import json,hashlib,threading,time

class TopologySnapshotReplicator:
    def __init__(self):
        self.snapshots={};self.lock=threading.RLock()
    def publish(self,workspace_id,version,payload):
        body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        digest=hashlib.sha256(body).hexdigest()
        row={"workspace_id":workspace_id,"version":int(version),"payload":payload,"hash":digest,"ts":time.time()}
        with self.lock:self.snapshots[workspace_id]=row
        return row
    def latest(self,workspace_id):
        with self.lock:return self.snapshots.get(workspace_id)
    def verify(self,row):
        body=json.dumps(row["payload"],sort_keys=True,separators=(",",":")).encode()
        return hashlib.sha256(body).hexdigest()==row["hash"]
