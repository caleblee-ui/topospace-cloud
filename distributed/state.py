
from __future__ import annotations
from abc import ABC, abstractmethod
import threading

class DistributedStateAdapter(ABC):
    @abstractmethod
    def get(self,key): raise NotImplementedError
    @abstractmethod
    def set(self,key,value,ttl=None): raise NotImplementedError
    @abstractmethod
    def delete(self,key): raise NotImplementedError

class InMemoryDistributedState(DistributedStateAdapter):
    def __init__(self):
        self.data={};self.lock=threading.RLock()
    def get(self,key):
        with self.lock:return self.data.get(key)
    def set(self,key,value,ttl=None):
        with self.lock:self.data[key]=value
    def delete(self,key):
        with self.lock:self.data.pop(key,None)
