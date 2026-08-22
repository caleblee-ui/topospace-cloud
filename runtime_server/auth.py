
import hmac
class APIKeyAuth:
    def __init__(self,keys=None):
        self.keys=dict(keys or {})
    def add(self,key_id,secret):
        self.keys[str(key_id)]=str(secret)
    def verify(self,key_id,secret):
        expected=self.keys.get(str(key_id))
        return expected is not None and hmac.compare_digest(expected,str(secret))
