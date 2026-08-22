
from runtime_server.service import RuntimeService
from runtime_platform.persistence import EventStore
from runtime_platform.idempotency import IdempotencyStore
from runtime_platform.rate_limit import TokenBucket
from runtime_platform.metering import UsageMeter
from runtime_platform.stream import TopologyEventStream
from runtime_platform.tracing import Tracer
class DistributedRuntimePlatform:
 def __init__(self,event_store=None):
  self.runtime=RuntimeService();self.events=event_store or EventStore();self.ids=IdempotencyStore();self.limiter=TokenBucket();self.meter=UsageMeter();self.stream=TopologyEventStream();self.tracer=Tracer()
 def dispatch(self,scope,hook,task,payload=None,idempotency_key=None):
  t=scope.tenant_id
  if not self.limiter.allow(t):return {"ok":False,"error":"rate_limited","status":429}
  if idempotency_key:
   c=self.ids.get((t,idempotency_key))
   if c is not None:return {**c,"idempotent_replay":True}
  span=self.tracer.start("topospace."+hook,{"tenant":t,"task":task})
  try:
   r=self.runtime.dispatch(scope,hook,task,payload or {});o={"ok":True,"result":r,"trace_id":span["trace_id"]}
   self.events.append(t,task,hook,payload or {});self.meter.record(t,"runtime_events");self.stream.publish(t,{"task_id":task,"hook":hook})
   if idempotency_key:self.ids.put((t,idempotency_key),o)
   return o
  finally:self.tracer.finish(span)
