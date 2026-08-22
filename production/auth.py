
from __future__ import annotations
import hashlib, hmac, secrets, time
from dataclasses import dataclass

@dataclass
class APIKeyRecord:
    key_id:str
    secret_hash:str
    created_at:float
    enabled:bool=True

class APIKeyManager:
    def __init__(self):
        self._keys={}

    @staticmethod
    def _hash(secret):
        return hashlib.sha256(secret.encode()).hexdigest()

    def create(self,key_id=None):
        key_id=key_id or secrets.token_hex(6)
        secret=secrets.token_urlsafe(32)
        self._keys[key_id]=APIKeyRecord(key_id,self._hash(secret),time.time(),True)
        return {"key_id":key_id,"secret":secret}

    def import_key(self,key_id,secret,enabled=True):
        self._keys[key_id]=APIKeyRecord(key_id,self._hash(secret),time.time(),enabled)

    def verify(self,key_id,secret):
        rec=self._keys.get(key_id)
        return bool(rec and rec.enabled and hmac.compare_digest(rec.secret_hash,self._hash(secret)))

    def disable(self,key_id):
        if key_id in self._keys:self._keys[key_id].enabled=False
