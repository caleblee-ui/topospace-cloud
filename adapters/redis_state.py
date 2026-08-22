
from distributed.state import DistributedStateAdapter

class RedisStateAdapter(DistributedStateAdapter):
    """Optional Redis adapter. Pass an instantiated redis-py client."""
    def __init__(self,client,prefix="topospace:"):
        self.client=client;self.prefix=prefix
    def _k(self,key):return self.prefix+key
    def get(self,key):
        v=self.client.get(self._k(key))
        return None if v is None else v
    def set(self,key,value,ttl=None):
        if ttl:self.client.setex(self._k(key),int(ttl),value)
        else:self.client.set(self._k(key),value)
    def delete(self,key):self.client.delete(self._k(key))
