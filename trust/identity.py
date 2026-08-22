
from __future__ import annotations
from dataclasses import dataclass,asdict
import time,hashlib,hmac,json,base64

@dataclass
class ServiceIdentity:
    service_id:str
    tenant_id:str
    audience:str
    expires_at:float
    roles:list

class ServiceIdentityIssuer:
    """Dependency-light signed service identity token."""
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret
    def issue(self,identity:ServiceIdentity):
        payload=json.dumps(asdict(identity),sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,payload,hashlib.sha256).hexdigest()
        body=base64.urlsafe_b64encode(payload).decode().rstrip("=")
        return body+"."+sig
    def verify(self,token,audience=None):
        body,sig=token.rsplit(".",1)
        body += "="*((4-len(body)%4)%4)
        payload=base64.urlsafe_b64decode(body.encode())
        exp=hmac.new(self.secret,payload,hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig,exp):raise ValueError("invalid_service_identity")
        obj=json.loads(payload)
        if obj["expires_at"]<time.time():raise ValueError("service_identity_expired")
        if audience and obj["audience"]!=audience:raise ValueError("service_identity_audience_mismatch")
        return ServiceIdentity(**obj)
