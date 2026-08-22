
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.hybrid_context import HybridTopologicalScorer
TASKS=[
{"name":"oauth","relevant":{"auth.py","oauth.py","auth_test.py"},"nodes":["auth.py","oauth.py","auth_test.py","layout.py"],"edges":[("auth.py","oauth.py",.1),("oauth.py","auth_test.py",.14),("auth.py","layout.py",.72)],"dist":{"auth.py":.10,"oauth.py":.14,"auth_test.py":.30,"layout.py":.12},"pers":{"auth.py":.8,"oauth.py":.72,"auth_test.py":.68,"layout.py":.08},"drift":{"auth.py":.08,"oauth.py":.10,"auth_test.py":.06,"layout.py":.44}},
{"name":"billing","relevant":{"billing.py","invoice.py","billing_test.py"},"nodes":["billing.py","invoice.py","billing_test.py","dashboard.py"],"edges":[("billing.py","invoice.py",.11),("invoice.py","billing_test.py",.15),("billing.py","dashboard.py",.69)],"dist":{"billing.py":.11,"invoice.py":.16,"billing_test.py":.31,"dashboard.py":.13},"pers":{"billing.py":.82,"invoice.py":.73,"billing_test.py":.66,"dashboard.py":.09},"drift":{"billing.py":.07,"invoice.py":.11,"billing_test.py":.08,"dashboard.py":.41}},
{"name":"cache","relevant":{"cache.py","redis.py","cache_test.py"},"nodes":["cache.py","redis.py","cache_test.py","metrics.py"],"edges":[("cache.py","redis.py",.09),("redis.py","cache_test.py",.13),("cache.py","metrics.py",.74)],"dist":{"cache.py":.10,"redis.py":.15,"cache_test.py":.29,"metrics.py":.12},"pers":{"cache.py":.84,"redis.py":.75,"cache_test.py":.70,"metrics.py":.07},"drift":{"cache.py":.06,"redis.py":.09,"cache_test.py":.07,"metrics.py":.47}}
]
def metric(sel,rel):
 s=set(sel);r=set(rel);tp=len(s&r);return {"precision":tp/len(s),"recall":tp/len(r),"success":1.0 if r.issubset(s) else 0.0}
def main():
 scorer=HybridTopologicalScorer();rows=[]
 for t in TASKS:
  baseline=sorted(t["dist"],key=t["dist"].get)[:3]
  hybrid=[x["id"] for x in scorer.score(t["nodes"],t["edges"],t["dist"],t["pers"],t["drift"])[:3]]
  for mode,sel in [("adaptive-distance",baseline),("hybrid-topological",hybrid)]:
   rows.append({"task":t["name"],"mode":mode,"selected":sel,**metric(sel,t["relevant"])})
 summary={}
 for mode in ("adaptive-distance","hybrid-topological"):
  rs=[r for r in rows if r["mode"]==mode];summary[mode]={k:sum(x[k] for x in rs)/len(rs) for k in ("precision","recall","success")}
 result={"rows":rows,"summary":summary};print(json.dumps(result,indent=2))
 assert summary["hybrid-topological"]["success"] > summary["adaptive-distance"]["success"]
 Path("benchmarks/v09_hybrid_result.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__":main()
