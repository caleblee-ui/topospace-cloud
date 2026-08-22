
from pathlib import Path
import sys,time,json,random,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from performance.topology_delta_runtime import TopologyDeltaRuntime
from performance.delta import TopologyDelta
from performance.incremental_neighborhood import IncrementalNeighborhood

N=20000
nodes=[{"id":f"n{i}","distance":(i%100)/100,"score":1-((i%80)/100),"drift":(i%20)/100} for i in range(N)]
edges=[(f"n{i}",f"n{i+1}",.1) for i in range(N-1)]

inc=TopologyDeltaRuntime(epsilon=.35,shards=32)
t=time.perf_counter();inc.bootstrap(nodes,edges);bootstrap_ms=(time.perf_counter()-t)*1000

updates=[{"id":f"n{i}","distance":.1,"score":.9,"drift":.05} for i in range(0,1000,10)]
delta=TopologyDelta(updated_nodes=updates)

times=[]
for _ in range(200):
    t=time.perf_counter();inc.apply(delta);times.append((time.perf_counter()-t)*1000)

full=IncrementalNeighborhood(epsilon=.35)
full_times=[]
for _ in range(30):
    t=time.perf_counter();full.rebuild(nodes);full_times.append((time.perf_counter()-t)*1000)

out={
 "objects":N,
 "delta_updates":len(updates),
 "bootstrap_ms":bootstrap_ms,
 "incremental_p50_ms":statistics.median(times),
 "incremental_p95_ms":sorted(times)[int(.95*len(times))-1],
 "full_rebuild_p50_ms":statistics.median(full_times),
 "speedup_vs_full_p50":statistics.median(full_times)/max(1e-9,statistics.median(times)),
 "note":"CPU/memory microbenchmark on deterministic local objects; not end-to-end production latency."
}
print(json.dumps(out,indent=2))
assert out["speedup_vs_full_p50"]>1
Path("results/v25_incremental_benchmark.json").write_text(json.dumps(out,indent=2))
