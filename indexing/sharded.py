
from __future__ import annotations
import hashlib, threading

class ShardedObjectIndex:
    def __init__(self,shards=16):
        self.shards=max(1,int(shards))
        self.data=[{} for _ in range(self.shards)]
        self.locks=[threading.RLock() for _ in range(self.shards)]

    def _sid(self,key):
        h=int(hashlib.blake2b(str(key).encode(),digest_size=8).hexdigest(),16)
        return h%self.shards

    def put(self,key,value):
        sid=self._sid(key)
        with self.locks[sid]:self.data[sid][key]=value

    def get(self,key):
        sid=self._sid(key)
        with self.locks[sid]:return self.data[sid].get(key)

    def delete(self,key):
        sid=self._sid(key)
        with self.locks[sid]:self.data[sid].pop(key,None)

    def batch_get(self,keys):
        return {k:self.get(k) for k in keys}

    def __len__(self):
        return sum(len(x) for x in self.data)
