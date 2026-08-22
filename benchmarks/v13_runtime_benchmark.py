
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.decision_runtime import TopoDecisionRuntime,Candidate

C=[
 Candidate("auth.py","code",.10,.8,.05),
 Candidate("oauth.py","code",.14,.72,.08),
 Candidate("auth_test.py","code",.30,.68,.06),
 Candidate("layout.py","code",.11,.05,.55),
 Candidate("grep","tool",.19,.4,.05),
 Candidate("browser","tool",.12,.05,.50),
 Candidate("security-review","skill",.21,.7,.08),
 Candidate("frontend-agent","agent",.13,.03,.48),
 Candidate("security-agent","agent",.24,.75,.05),
]
E=[
 ("auth.py","oauth.py",.10),("oauth.py","auth_test.py",.14),("auth.py","layout.py",.75),
 ("grep","auth.py",.18),("security-review","auth.py",.20),
 ("security-agent","security-review",.12),("frontend-agent","layout.py",.10)
]
def main():
 r=TopoDecisionRuntime()
 code=r.select(C,E,3,["code"])
 tools=r.select(C,E,1,["tool"])
 agents=r.select(C,E,1,["agent"])
 out={
  "code":[x["id"] for x in code.selected],
  "tools":[x["id"] for x in tools.selected],
  "agents":[x["id"] for x in agents.selected]
 }
 print(json.dumps(out,indent=2))
 assert out["code"]==["auth.py","oauth.py","auth_test.py"]
 assert out["tools"][0]=="grep"
 assert out["agents"][0]=="security-agent"
 Path("benchmarks/v13_runtime_result.json").write_text(json.dumps(out,indent=2))
if __name__=="__main__":main()
