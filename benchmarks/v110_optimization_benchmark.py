
from pathlib import Path
import sys,json,random,statistics,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from optimization_v2.engine import OptimizationEngineV2

rng=random.Random(1729)
engine=OptimizationEngineV2()
reductions=[];recalls=[];lat=[]
for run in range(500):
    items=[]
    relevant=set()
    for i in range(120):
        rel=i<12
        if rel:relevant.add(f"n{i}")
        distance=max(0,min(1,rng.gauss(.16,.07) if rel else rng.gauss(.65,.18)))
        score=max(0,min(1,rng.gauss(.88,.08) if rel else rng.gauss(.32,.16)))
        utility=max(0,min(1,rng.gauss(.82,.1) if rel else rng.gauss(.4,.2)))
        items.append({"id":f"n{i}","distance":distance,"score":score,"utility":utility,"drift":rng.random()*.2,"tokens":rng.randint(80,260)})
    t=time.perf_counter();out=engine.optimize(items,token_budget=4200);lat.append((time.perf_counter()-t)*1000)
    chosen={x["id"] for x in out["context"]}
    recalls.append(len(chosen&relevant)/len(relevant))
    reductions.append(out["token_reduction"])

# consolidation fixture
mem=[]
for i in range(30):
    base=i//3
    mem.append({"id":f"m{i}","content":f"oauth refresh token policy group{base} common","importance":.5+i/100,"semantic_score":.8})
compact=engine.consolidate_memory(mem)
out={
 "runs":500,
 "mean_token_reduction":statistics.mean(reductions),
 "median_token_reduction":statistics.median(reductions),
 "mean_relevant_recall":statistics.mean(recalls),
 "p95_engine_ms":sorted(lat)[int(.95*len(lat))-1],
 "memory_records_before":len(mem),
 "memory_records_after":len(compact),
 "note":"Synthetic topology-routing benchmark; marketing claims require representative real workloads."
}
print(json.dumps(out,indent=2))
assert out["mean_token_reduction"]>.45
assert out["mean_relevant_recall"]>.85
Path("results/v110_optimization_benchmark.json").write_text(json.dumps(out,indent=2))
