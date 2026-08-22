
from __future__ import annotations
import json,hmac,hashlib,base64,time

class PolicySigner:
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret

    def sign(self,tenant_id,task_type,version,payload):
        envelope={
          "tenant_id":tenant_id,
          "task_type":task_type,
          "version":int(version),
          "payload":payload,
          "signed_at":time.time(),
        }
        body=json.dumps(envelope,sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        token=base64.urlsafe_b64encode(body).decode().rstrip("=")+"."+sig
        return {"envelope":envelope,"token":token}

    def verify(self,token):
        body64,sig=token.rsplit(".",1)
        padded=body64+"="*((4-len(body64)%4)%4)
        body=base64.urlsafe_b64decode(padded.encode())
        exp=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig,exp):
            raise ValueError("invalid_policy_signature")
        return json.loads(body)
