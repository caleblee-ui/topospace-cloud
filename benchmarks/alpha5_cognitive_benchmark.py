
from pathlib import Path
import sys,random,json,statistics,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cognitive_topology.runtime import TopologicalCognitiveRuntime

rng=random.Random(1729);promoted=[];recall_hits=[];lat=[]
for run in range(300):
 r=TopologicalCognitiveRuntime()
 relevant=set()
 for i in range(80):
  rel=i<8
  if rel:relevant.add(f"m{i}")
  r.remember(f"m{i}",f"memory {i}",importance=rng.uniform(.75,.98) if rel else rng.uniform(.1,.65),
             confidence=rng.uniform(.8,.98) if rel else rng.uniform(.1,.7),
             utility=rng.uniform(.78,.98) if rel else rng.uniform(.1,.65),
             distance=rng.uniform(.03,.2) if rel else rng.uniform(.3,.95),
             metadata={"tokens":rng.randint(70,180)})
 for mid in relevant:
  for _ in range(7):r.record_use(mid,True,1)
 moved=r.consolidate();promoted.append(sum(1 for x in moved if x["to"]=="semantic"))
 t=time.perf_counter();out=r.recall(token_budget=1800,limit=12);lat.append((time.perf_counter()-t)*1000)
 chosen={m.id for m in out["memories"]};recall_hits.append(len(chosen&relevant)/len(relevant))
out={"runs":300,"mean_semantic_promotions":statistics.mean(promoted),"mean_relevant_recall":statistics.mean(recall_hits),"p95_layered_recall_ms":sorted(lat)[int(.95*len(lat))-1],"note":"Synthetic cognitive-memory regression; not human-memory or external agent-quality evidence."}
print(json.dumps(out,indent=2));assert out["mean_relevant_recall"]>.95 and out["mean_semantic_promotions"]>=7
Path("results/alpha5_cognitive_benchmark.json").write_text(json.dumps(out,indent=2))
