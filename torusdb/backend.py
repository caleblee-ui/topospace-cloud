
from abc import ABC, abstractmethod
from torusdb.models import MemoryRecord

class TorusMemoryBackend(ABC):
    """Backend contract for TorusDB Agent Memory integration.

    The interface does not assume plaintext storage. Ciphertext/opaque payloads may be
    stored and returned unchanged while searchable metadata/features remain separate.
    """
    @abstractmethod
    def upsert(self,record:MemoryRecord): raise NotImplementedError
    @abstractmethod
    def get(self,memory_id:str): raise NotImplementedError
    @abstractmethod
    def search(self,query:str,limit:int=50,filters=None): raise NotImplementedError
    @abstractmethod
    def delete(self,memory_id:str): raise NotImplementedError
