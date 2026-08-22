
import json,hmac,hashlib
from dataclasses import asdict

class SignedConfig:
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret

    def sign(self,config,version):
        payload={"version":int(version),"config":asdict(config)}
        body=json.dumps(payload,sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return {"payload":payload,"signature":sig}

    def verify(self,bundle):
        body=json.dumps(bundle["payload"],sort_keys=True,separators=(",",":")).encode()
        expected=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return hmac.compare_digest(expected,bundle.get("signature",""))
