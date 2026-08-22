
from pathlib import Path
import sys,time,statistics,json,tempfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime_platform.service import DistributedRuntimePlatform
from runtime_platform.persistence import EventStore
from runtime_server.tenant import TenantScope
with tempfile.TemporaryDirectory() as d:
 p=DistributedRuntimePlatform(EventStore(d+"/e.db"));s=TenantScope("bench");xs=[]
 for i in range(1000):
  a=time.perf_counter();o=p.dispatch(s,"task_start",f"t{i}",{},idempotency_key=f"k{i}");assert o["ok"];xs.append((time.perf_counter()-a)*1000)
 out={"runs":1000,"mean_persistent_dispatch_ms":statistics.mean(xs),"p95_persistent_dispatch_ms":sorted(xs)[949],"events":p.events.count("bench"),"metered":p.meter.snapshot("bench")["runtime_events"],"note":"Local SQLite reference persistence; external Redis/PostgreSQL/network latency not measured."}
 print(json.dumps(out,indent=2));assert out["events"]==1000 and out["metered"]==1000 and out["p95_persistent_dispatch_ms"]<10
 Path("results/beta2_platform_benchmark.json").write_text(json.dumps(out,indent=2))
