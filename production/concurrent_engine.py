
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from threading import RLock
from production.adaptive_engine import AdaptiveTopoSpaceEngine

class ConcurrentTopoSpaceEngine:
    def __init__(self,engine=None,max_workers=8):
        self.engine=engine or AdaptiveTopoSpaceEngine()
        self.pool=ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix="topospace")
        self.lock=RLock()

    def optimize(self,*args,**kwargs):
        return self.engine.optimize_adaptive(*args,**kwargs)

    def submit(self,*args,**kwargs):
        return self.pool.submit(self.engine.optimize_adaptive,*args,**kwargs)

    def health(self):
        with self.lock:return self.engine.health()

    def shutdown(self,wait=True):
        self.pool.shutdown(wait=wait)
