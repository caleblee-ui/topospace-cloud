from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import json
@dataclass
class TopologyEvent:event:str;workspace_id:str;payload:dict;timestamp:str
class EventBus:
 def __init__(self):self.events=[]
 def publish(self,event,workspace_id,payload):
  x=TopologyEvent(event,workspace_id,payload,datetime.now(timezone.utc).isoformat());self.events.append(x);return x
def sse_encode(x):return f'event: {x.event}\ndata: {json.dumps(asdict(x))}\n\n'
