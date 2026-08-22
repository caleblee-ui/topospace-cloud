
import hashlib,hmac,time
class APIKeyStore:
    def __init__(self):self.keys={}
    @staticmethod
    def digest(raw):return hashlib.sha256(raw.encode()).hexdigest()
    def issue(self,tenant_id,raw_key,scopes=("inference",)):
        self.keys[self.digest(raw_key)]={"tenant_id":tenant_id,"scopes":set(scopes),"active":True}
    def authenticate(self,raw_key,scope="inference"):
        row=self.keys.get(self.digest(raw_key))
        if not row or not row["active"] or scope not in row["scopes"]:raise PermissionError("invalid_api_key")
        return row
