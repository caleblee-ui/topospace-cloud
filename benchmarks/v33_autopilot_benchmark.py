
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from autopilot.runtime import AutopilotRuntime
from autopilot.models import RuntimeSignals

a=AutopilotRuntime()
scenarios=[
 ("easy",RuntimeSignals(.98,.10,.05,.90,.70,0,.90)),
 ("normal",RuntimeSignals(.90,.35,.15,.50,.30,.05,.72)),
 ("degraded",RuntimeSignals(.62,.82,.55,.45,.50,.35,.32)),
 ("recovering",RuntimeSignals(.82,.45,.25,.60,.35,.10,.68)),
]
rows=[]
for name,s in scenarios:
 r=a.update(s);rows.append({"name":name,**r})
print(json.dumps(rows,indent=2))
easy=rows[0]["decision"];bad=rows[2]["decision"]
assert bad["epsilon"]>easy["epsilon"]
assert bad["max_context_tokens"]>easy["max_context_tokens"]
assert bad["memory_recall_limit"]>easy["memory_recall_limit"]
Path("results/v33_autopilot_benchmark.json").write_text(json.dumps(rows,indent=2))
