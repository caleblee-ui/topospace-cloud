
from __future__ import annotations
from dataclasses import dataclass,asdict
import json,hmac,hashlib,time,base64

@dataclass
class License:
    customer_id:str
    edition:str
    expires_at:float
    max_tenants:int=1
    max_nodes:int=3
    features:list|None=None

class LicenseManager:
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret

    def issue(self,license_obj:License):
        payload=json.dumps(asdict(license_obj),sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,payload,hashlib.sha256).hexdigest()
        body=base64.urlsafe_b64encode(payload).decode().rstrip("=")
        return body+"."+sig

    def verify(self,token):
        body,sig=token.rsplit(".",1)
        padded=body+"="*((4-len(body)%4)%4)
        payload=base64.urlsafe_b64decode(padded.encode())
        expected=hmac.new(self.secret,payload,hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig,expected): raise ValueError("invalid_license_signature")
        obj=json.loads(payload)
        if float(obj["expires_at"])<time.time(): raise ValueError("license_expired")
        return License(**obj)
