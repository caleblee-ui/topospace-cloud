
from dataclasses import replace
import threading
class RollingConfig:
    def __init__(self,config):
        self._config=config;self.version=1;self.lock=threading.RLock()
    def get(self):
        with self.lock:return self.version,self._config
    def update(self,**changes):
        with self.lock:
            self._config=replace(self._config,**changes);self.version+=1
            return self.version,self._config
