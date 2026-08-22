
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from multiagent.models import AgentNode
from multiagent.orchestrator import AdaptiveMultiAgentRuntime

def main():
    agents=[
      AgentNode("coding-agent",["code","debug"],.10,.80,.05,.20,.10,.95),
      AgentNode("security-agent",["security","review"],.20,.78,.04,.25,.08,.97),
      AgentNode("test-agent",["test","verification"],.22,.72,.06,.18,.05,.96),
      AgentNode("frontend-agent",["frontend"],.11,.08,.50,.15,.10,.90),
    ]
    edges=[
      ("coding-agent","security-agent",.16),
      ("coding-agent","test-agent",.14),
      ("coding-agent","frontend-agent",.72),
      ("security-agent","test-agent",.18),
    ]

    def executor(payload,step):
        team={x["id"] for x in payload["team"]}
        need={"coding-agent","security-agent","test-agent"}
        return {
          "success":need.issubset(team),
          "message":"team complete" if need.issubset(team) else "verification specialist missing",
          "token_cost_norm":.3,
          "latency_norm":.25,
          "tool_calls_norm":.2,
          "risk":.08
        }

    runtime=AdaptiveMultiAgentRuntime(max_steps=3,drift_threshold=.2)
    out=runtime.run("Fix and verify OAuth authentication vulnerability",agents,edges,executor,
                    required_capabilities=["code","security","test"])
    summary={
      "success":out["success"],
      "steps":len(out["steps"]),
      "teams":[[a["id"] for a in s["team"]] for s in out["steps"]],
      "drift":[s["team_drift"] for s in out["steps"]],
      "reward":[s["reward"] for s in out["steps"]],
    }
    print(json.dumps(summary,indent=2))
    assert summary["success"]
    assert {"coding-agent","security-agent","test-agent"}.issubset(set(summary["teams"][0]))
    Path("benchmarks/v15_multiagent_result.json").write_text(json.dumps(summary,indent=2))
if __name__=="__main__":main()
