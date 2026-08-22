
from __future__ import annotations
import json,time,hashlib
from pathlib import Path

class PolicyDisasterRecovery:
    def export_bundle(self,path,policies,lineage):
        bundle={
          "created_at":time.time(),
          "policies":policies,
          "lineage":lineage,
        }
        raw=json.dumps(bundle,sort_keys=True,indent=2).encode()
        wrapper={"sha256":hashlib.sha256(raw).hexdigest(),"payload":bundle}
        Path(path).write_text(json.dumps(wrapper,sort_keys=True,indent=2))
        return wrapper

    def restore_bundle(self,path):
        wrapper=json.loads(Path(path).read_text())
        raw=json.dumps(wrapper["payload"],sort_keys=True,indent=2).encode()
        if hashlib.sha256(raw).hexdigest()!=wrapper["sha256"]:
            raise ValueError("backup_checksum_mismatch")
        return wrapper["payload"]
