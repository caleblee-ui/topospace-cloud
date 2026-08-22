
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.topological_agent import TopologicalAgentRuntime
from runtime.decision_runtime import Candidate

candidates=[
 Candidate("auth.py","code",.10,.8,.05),
 Candidate("oauth.py","code",.14,.72,.08),
 Candidate("auth_test.py","code",.30,.68,.06),
 Candidate("layout.py","code",.11,.05,.55),
 Candidate("grep","tool",.19,.4,.05),
 Candidate("browser","tool",.12,.05,.50),
 Candidate("security-review","skill",.21,.7,.08),
 Candidate("security-agent","agent",.24,.75,.05),
]
edges=[
 ("auth.py","oauth.py",.10),("oauth.py","auth_test.py",.14),("auth.py","layout.py",.75),
 ("grep","auth.py",.18),("security-review","auth.py",.20),("security-agent","security-review",.12)
]

def executor(payload):
 print("VISIBLE CONTEXT:")
 for typ,items in payload["context"].items():
  print(typ,[x["id"] for x in items])
 return {"success":True,"action":"inspect auth.py and run tests"}

agent=TopologicalAgentRuntime()
print(agent.step("Fix OAuth authentication bug",candidates,edges,executor))
