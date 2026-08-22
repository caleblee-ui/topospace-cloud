
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent.autonomous_topological_agent import AutonomousTopologicalAgent
from runtime.decision_runtime import Candidate

candidates=[
 Candidate("auth.py","code",.10,.8,.05),
 Candidate("oauth.py","code",.14,.72,.08),
 Candidate("grep","tool",.18,.4,.05),
]
edges=[("auth.py","oauth.py",.10),("grep","auth.py",.18)]

def executor(payload,step):
    code=[x["id"] for x in payload["context"]["code"]]
    print("STEP",step,"VISIBLE CODE",code)
    return {
      "success":"auth_test.py" in code,
      "message":"pass" if "auth_test.py" in code else "test context missing",
      "token_cost_norm":.3,
      "latency_norm":.25,
      "tool_calls_norm":.25,
      "risk":.1
    }

def mutate(cands,edges,obs,step):
    if not obs["success"]:
        cands=cands+[Candidate("auth_test.py","code",.27,.72,.04)]
        edges=edges+[("oauth.py","auth_test.py",.12)]
    return cands,edges

result=AutonomousTopologicalAgent().execute(
 "Fix OAuth authentication bug",candidates,edges,executor,mutate
)
print("SUCCESS",result["success"])
