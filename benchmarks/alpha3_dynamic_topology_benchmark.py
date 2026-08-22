
from pathlib import Path
import sys,random,time,statistics,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from dynamic_topology.runtime import DynamicTopologyRuntime
rng=random.Random(1729);lat=[];correct=0
for run in range(500):
 r=DynamicTopologyRuntime();r.add("task","task",score=1,distance=0)
 best=None;bestval=-1
 for kind,n in [("memory",20),("context",15),("tool",10),("agent",8)]:
  for i in range(n):
   ident=f"{kind}-{i}";score=rng.random();distance=rng.random();weight=rng.random()
   r.add(ident,kind,score=score,distance=distance);r.link("task",ident,"candidate",weight)
   bonus={"memory":.05,"context":.04,"tool":.08,"agent":.07}[kind]
   val=.42*score+.33*(1-distance)+.20*weight+bonus
   if val>bestval:bestval=val;best=ident
 t=time.perf_counter();plan=r.execute_plan("task",8)["plan"];lat.append((time.perf_counter()-t)*1000)
 if plan and plan[0]["to"]==best:correct+=1
out={"runs":500,"top1_planner_accuracy":correct/500,"p95_plan_ms":sorted(lat)[int(.95*len(lat))-1],"mean_plan_ms":statistics.mean(lat),"note":"Synthetic graph-planning regression; not external workload evidence."}
print(json.dumps(out,indent=2));assert out["top1_planner_accuracy"]>.99
Path("results/alpha3_dynamic_topology_benchmark.json").write_text(json.dumps(out,indent=2))
