
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from runtime.closed_loop import ClosedLoopTopoAgent
from runtime.decision_runtime import Candidate

def main():
    candidates=[
      Candidate("auth.py","code",.10,.8,.05),
      Candidate("oauth.py","code",.14,.72,.08),
      Candidate("layout.py","code",.11,.05,.55),
      Candidate("grep","tool",.18,.4,.05),
      Candidate("browser","tool",.12,.05,.5)
    ]
    edges=[
      ("auth.py","oauth.py",.10),
      ("auth.py","layout.py",.76),
      ("grep","auth.py",.18)
    ]

    def executor(payload,step):
        code=[x["id"] for x in payload["context"].get("code",[])]
        if "auth_test.py" in code:
            return {"success":True,"message":"tests pass","token_cost_norm":.25,"latency_norm":.2,"tool_calls_norm":.25,"risk":.1}
        return {"success":False,"message":"missing failing test context","token_cost_norm":.45,"latency_norm":.35,"tool_calls_norm":.4,"risk":.2}

    def mutate(cands,edges,obs,step):
        ids={c.id for c in cands}
        if not obs.get("success") and "auth_test.py" not in ids:
            cands=cands+[Candidate("auth_test.py","code",.28,.70,.04)]
            edges=edges+[("oauth.py","auth_test.py",.13)]
        return cands,edges

    agent=ClosedLoopTopoAgent(max_steps=4,drift_threshold=.2)
    out=agent.run("Fix OAuth authentication bug and pass tests",candidates,edges,executor,mutate)
    summary={
      "success":out["success"],
      "steps":len(out["steps"]),
      "drift_scores":[x["drift_score"] for x in out["steps"]],
      "replanned":[x["replanned"] for x in out["steps"]],
      "selected_code":[[n["id"] for n in x["selected"]["code"]] for x in out["steps"]],
      "final_topology":out["final_topology"]
    }
    print(json.dumps(summary,indent=2))
    assert summary["success"] is True
    assert summary["steps"]==2
    assert "auth_test.py" in summary["selected_code"][-1]
    assert summary["replanned"][0] is True
    Path("benchmarks/v14_closed_loop_result.json").write_text(json.dumps(summary,indent=2))
if __name__=="__main__":main()
