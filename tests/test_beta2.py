
from runtime_platform.service import DistributedRuntimePlatform
from runtime_platform.persistence import EventStore
from runtime_server.tenant import TenantScope
def test_persist(tmp_path):
 e=EventStore(str(tmp_path/"x.db"));p=DistributedRuntimePlatform(e);s=TenantScope("a");p.dispatch(s,"task_start","t",{});assert e.count("a")==1
def test_idempotency():
 p=DistributedRuntimePlatform();s=TenantScope("a");a=p.dispatch(s,"task_start","t",{},idempotency_key="k");b=p.dispatch(s,"task_start","t",{},idempotency_key="k");assert b["idempotent_replay"] and a["trace_id"]==b["trace_id"]
def test_meter_stream():
 p=DistributedRuntimePlatform();s=TenantScope("a");q=p.stream.subscribe("a");p.dispatch(s,"task_start","t",{});assert p.meter.snapshot("a")["runtime_events"]==1 and q.get(timeout=.1)["task_id"]=="t"
def test_policy(tmp_path):
 e=EventStore(str(tmp_path/"x.db"));e.set_policy("a","epsilon",{"max":.4});assert e.policy("a","epsilon")["max"]==.4
