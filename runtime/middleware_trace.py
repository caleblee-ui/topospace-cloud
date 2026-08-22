
from __future__ import annotations
from dataclasses import dataclass,asdict
from time import time

@dataclass
class MiddlewareTraceEvent:
    seq:int
    phase:str
    payload:dict
    ts:float

class MiddlewareTrace:
    def __init__(self):
        self.seq=0;self.events=[]

    def add(self,phase,**payload):
        self.seq+=1
        e=MiddlewareTraceEvent(self.seq,phase,payload,time())
        self.events.append(e)
        return asdict(e)

    def export(self):
        return [asdict(x) for x in self.events]
