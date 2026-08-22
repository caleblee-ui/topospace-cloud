
import json,time,urllib.request
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.agent_graph_runtime import AgentGraphRuntime

BASE="http://localhost:8787"; W="demo"
r=AgentGraphRuntime(W)
frames=[
 r.upsert_node("task","OAuth migration","state",1),
 r.upsert_node("auth.py","auth.py","code",.94),
 r.connect("task","auth.py",.10,"topological"),
 r.upsert_node("oauth.py","oauth.py","code",.86),
 r.connect("auth.py","oauth.py",.14,"dependency"),
 r.upsert_node("auth_test.py","auth_test.py","test",.76),
 r.connect("oauth.py","auth_test.py",.18,"test"),
]
for f in frames:
 req=urllib.request.Request(f"{BASE}/workspaces/{W}/graph",data=json.dumps(f).encode(),headers={"Content-Type":"application/json"},method="POST")
 print(urllib.request.urlopen(req).read().decode());time.sleep(.7)
