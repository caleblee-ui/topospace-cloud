
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from general_geometry.views import ViewValue
from general_geometry.engine import GeneralizedGeometryEngine
from general_geometry.profiles import *
rng=random.Random(1729)
profiles={"lp1":exploratory_profile(),"lp2":balanced_profile(),"chebyshev":hard_constraint_profile(),"nested":hierarchical_agent_profile()}
summary={}
rank_signatures={}
for name,agg in profiles.items():
 selected_counts=[];violations=0;prec=[];rank_signatures[name]=[]
 eng=GeneralizedGeometryEngine(agg)
 for run in range(500):
  cs=[]
  for i in range(30):
   rel=i<6
   vals=[
    rng.uniform(.03,.2) if rel else rng.uniform(.2,.9),
    rng.uniform(.03,.25) if rel else rng.uniform(.15,.9),
    rng.uniform(.05,.3) if rel else rng.uniform(.15,.9),
    1.0 if (not rel and rng.random()<.2) else 0.0,
    1.0 if (not rel and rng.random()<.15) else 0.0,
    rng.uniform(.05,.5),
    rng.uniform(.02,.25) if rel else rng.uniform(.1,.7)]
   c={"id":f"{run}:{i}","relevant":rel,"violate":vals[3]>0 or vals[4]>0,
      "views":[ViewValue(str(j),x,1) for j,x in enumerate(vals)]}
   cs.append(c)
  vals=[(eng.distance(c["views"])["distance"],c) for c in cs]
  vals.sort(key=lambda x:x[0])
  if run<10:rank_signatures[name].append([c["id"] for _,c in vals[:5]])
  # profile-specific calibrated radius, to compare behavior not force common scaling
  eps={"lp1":.65,"lp2":.65,"chebyshev":.75,"nested":.55}[name]
  chosen=[c for d,c in vals if d<eps]
  selected_counts.append(len(chosen));violations+=sum(c["violate"] for c in chosen)
  if chosen:prec.append(sum(c["relevant"] for c in chosen)/len(chosen))
 summary[name]={"mean_selected":statistics.mean(selected_counts),"mean_precision":statistics.mean(prec) if prec else 0,
                "policy_security_violations_selected":violations}
# ranking should genuinely differ across operational geometries
different=sum(rank_signatures["lp1"][i]!=rank_signatures["nested"][i] for i in range(10))
out={"profiles":summary,"lp1_vs_nested_top5_different_queries":different,
     "note":"Synthetic geometry-behavior benchmark. Different admissible aggregators intentionally encode different operational preferences; no universal precision dominance is claimed."}
print(json.dumps(out,indent=2))
assert different>=5
assert summary["chebyshev"]["policy_security_violations_selected"]==0
assert summary["nested"]["policy_security_violations_selected"]==0
Path("results/beta4_general_geometry_benchmark.json").write_text(json.dumps(out,indent=2))
