
from __future__ import annotations
import json
def evaluate(result, relevant):
    relevant=set(relevant)
    out={}
    for key in ("semantic","hybrid"):
        ranked=[x[0] if isinstance(x,(list,tuple)) else x for x in result.get(key,[])]
        hits=[x for x in ranked if x in relevant]
        out[key]={"precision_at_k":len(hits)/len(ranked) if ranked else 0.0,
                  "recall_at_k":len(hits)/len(relevant) if relevant else 0.0,
                  "hits":hits}
    return out
if __name__=="__main__":
    import sys
    result=json.load(open(sys.argv[1])); relevant=json.load(open(sys.argv[2]))
    print(json.dumps(evaluate(result,relevant),indent=2))
