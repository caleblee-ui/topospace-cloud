
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from collective_topology.runtime import CollectiveTopologyRuntime

rng=random.Random(1729)
without=[];with_shared=[]
for run in range(300):
 r=CollectiveTopologyRuntime()
 producer=r.register_agent("producer","tenant",["security"])
 consumer=r.register_agent("consumer","tenant",["security"])
 # consumer local baseline has weak security candidates
 local=[rng.uniform(.35,.65) for _ in range(8)]
 without.append(max(local))
 # producer contributes successful security patterns
 patterns=[]
 for i in range(6):
  patterns.append({"id":f"p{run}-{i}","kind":"execution_pattern","tags":["security"],"success_rate":rng.uniform(.85,.98),"reward":rng.uniform(.82,.98)})
 r.publish_success("producer",patterns)
 r.sync_agent("consumer",6)
 imported=[x["score"] for x in consumer.local_nodes.values()]
 with_shared.append(max(local+imported))
out={
 "runs":300,
 "mean_best_local_score":statistics.mean(without),
 "mean_best_with_collective":statistics.mean(with_shared),
 "mean_gain":statistics.mean(with_shared)-statistics.mean(without),
 "note":"Synthetic cross-agent transfer regression; not external multi-agent quality evidence."
}
print(json.dumps(out,indent=2))
assert out["mean_best_with_collective"]>out["mean_best_local_score"]
Path("results/alpha6_collective_benchmark.json").write_text(json.dumps(out,indent=2))
