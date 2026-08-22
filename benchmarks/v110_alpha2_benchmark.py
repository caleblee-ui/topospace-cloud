
from pathlib import Path
import sys,random,time,statistics,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from optimization_v2.adaptive_engine import AdaptiveOptimizationEngine

rng=random.Random(314159);reductions=[];recalls=[];cold=[];warm=[];ps=[];eps=[]
for run in range(400):
 e=AdaptiveOptimizationEngine();items=[];relevant=set()
 for i in range(100):
  rel=i<10
  if rel:relevant.add(str(i))
  items.append({"id":str(i),"content":"agent memory "+str(i),"distance":max(.01,min(1,rng.gauss(.13,.05) if rel else rng.gauss(.62,.18))),"score":max(0,min(1,rng.gauss(.9,.06) if rel else rng.gauss(.3,.15))),"utility":max(0,min(1,rng.gauss(.85,.08) if rel else rng.gauss(.4,.18))),"tokens":rng.randint(80,240)})
 t=time.perf_counter();o=e.optimize("agent task",items,3600);cold.append((time.perf_counter()-t)*1000)
 t=time.perf_counter();w=e.optimize("agent task",items,3600);warm.append((time.perf_counter()-t)*1000)
 chosen={x["id"] for x in o["context"]};recalls.append(len(chosen&relevant)/10);reductions.append(o["token_reduction"]);ps.append(o["p"]);eps.append(o["epsilon"])
out={"runs":400,"mean_token_reduction":statistics.mean(reductions),"mean_relevant_recall":statistics.mean(recalls),"cold_p95_ms":sorted(cold)[int(.95*len(cold))-1],"warm_cache_p95_ms":sorted(warm)[int(.95*len(warm))-1],"mean_p":statistics.mean(ps),"mean_epsilon":statistics.mean(eps),"note":"Synthetic benchmark; not a production marketing claim."}
print(json.dumps(out,indent=2));assert out["mean_relevant_recall"]>.9 and out["mean_token_reduction"]>.45
Path("results/v110_alpha2_benchmark.json").write_text(json.dumps(out,indent=2))
