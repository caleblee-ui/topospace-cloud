
from abc import ABC, abstractmethod
import os

class SecretProvider(ABC):
    @abstractmethod
    def get(self,name): raise NotImplementedError

class EnvSecretProvider(SecretProvider):
    def get(self,name):
        value=os.getenv(name)
        if value is None: raise KeyError(name)
        return value

class MemorySecretProvider(SecretProvider):
    def __init__(self,values=None): self.values=dict(values or {})
    def get(self,name):
        if name not in self.values: raise KeyError(name)
        return self.values[name]
