
from pathlib import Path
import sys,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.persistent_agent_context import PersistentAgentContext

TASKS=[
 {"name":"oauth","relevant":{"auth.py","oauth.py","auth_test.py"},
  "semantic":["layout.py","auth.py","oauth.py"],"adaptive":["auth.py","oauth.py","layout.py"],
  "edges":[("auth.py","oauth.py",.10),("oauth.py","auth_test.py",.14),("auth.py","layout.py",.72)]},
 {"name":"billing","relevant":{"billing.py","invoice.py","billing_test.py"},
  "semantic":["dashboard.py","billing.py","invoice.py"],"adaptive":["billing.py","invoice.py","dashboard.py"],
  "edges":[("billing.py","invoice.py",.11),("invoice.py","billing_test.py",.16),("billing.py","dashboard.py",.68)]},
 {"name":"cache","relevant":{"cache.py","redis.py","cache_test.py"},
  "semantic":["metrics.py","cache.py","redis.py"],"adaptive":["cache.py","redis.py","metrics.py"],
  "edges":[("cache.py","redis.py",.09),("redis.py","cache_test.py",.13),("cache.py","metrics.py",.73)]}
]

def metrics(selected,relevant):
    s=set(selected);r=set(relevant);tp=len(s&r)
    return {"precision":tp/len(s) if s else 0,"recall":tp/len(r) if r else 0,"success":1.0 if r.issubset(s) else 0.0}

def main():
    persistent=PersistentAgentContext()
    rows=[]
    for t in TASKS:
        nodes=sorted(set(sum(([a,b] for a,b,_ in t["edges"]),[])))
        ctx=persistent.build(nodes,t["edges"],[.08,.10,.12,.14,.16,.30,.75])
        ranked=[n for n,_ in ctx["ranking"][:3]]
        for mode,sel in [("semantic",t["semantic"]),("adaptive",t["adaptive"]),("persistent",ranked)]:
            m=metrics(sel,t["relevant"])
            rows.append({"task":t["name"],"mode":mode,"selected":sel,**m})
    summary={}
    for mode in ("semantic","adaptive","persistent"):
        rs=[r for r in rows if r["mode"]==mode]
        summary[mode]={k:sum(r[k] for r in rs)/len(rs) for k in ("precision","recall","success")}
    result={"rows":rows,"summary":summary}
    print(json.dumps(result,indent=2))
    assert summary["persistent"]["recall"] >= summary["semantic"]["recall"]
    Path("benchmarks/v08_three_way_result.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__":main()
