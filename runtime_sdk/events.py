
from dataclasses import dataclass,field
import time
@dataclass
class RuntimeEvent:
    hook:str
    task_id:str
    agent_id:str|None=None
    payload:dict=field(default_factory=dict)
    ts:float=field(default_factory=time.time)
