
from __future__ import annotations
import json,hashlib,hmac,time

class PolicyAttestor:
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret

    def attest(self,policy_hash,runtime_version,tenant_id,metadata=None):
        statement={
          "policy_hash":policy_hash,
          "runtime_version":runtime_version,
          "tenant_id":tenant_id,
          "metadata":metadata or {},
          "issued_at":time.time(),
        }
        body=json.dumps(statement,sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return {"statement":statement,"signature":sig}

    def verify(self,attestation):
        body=json.dumps(attestation["statement"],sort_keys=True,separators=(",",":")).encode()
        exp=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return hmac.compare_digest(exp,attestation.get("signature",""))
