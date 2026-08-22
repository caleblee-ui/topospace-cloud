
from __future__ import annotations
from pathlib import Path
import hashlib,hmac,json,time

class ReleaseSigner:
    def __init__(self,secret):
        self.secret=secret.encode() if isinstance(secret,str) else secret

    def sign_file(self,path):
        p=Path(path);digest=hashlib.sha256(p.read_bytes()).hexdigest()
        statement={"file":p.name,"sha256":digest,"signed_at":time.time()}
        body=json.dumps(statement,sort_keys=True,separators=(",",":")).encode()
        sig=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return {"statement":statement,"signature":sig}

    def verify_file(self,path,bundle):
        p=Path(path);digest=hashlib.sha256(p.read_bytes()).hexdigest()
        if digest!=bundle["statement"]["sha256"]:return False
        body=json.dumps(bundle["statement"],sort_keys=True,separators=(",",":")).encode()
        exp=hmac.new(self.secret,body,hashlib.sha256).hexdigest()
        return hmac.compare_digest(exp,bundle["signature"])
