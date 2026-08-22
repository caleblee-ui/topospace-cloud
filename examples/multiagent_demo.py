
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from multiagent.models import AgentNode
from multiagent.orchestrator import AdaptiveMultiAgentRuntime

agents=[
 AgentNode("coding-agent",["code","debug"],.1,.8,.05),
 AgentNode("security-agent",["security"],.2,.75,.05),
 AgentNode("test-agent",["test"],.22,.72,.05),
 AgentNode("frontend-agent",["frontend"],.12,.05,.5),
]
edges=[
 ("coding-agent","security-agent",.15),
 ("coding-agent","test-agent",.12),
 ("coding-agent","frontend-agent",.75),
]

def executor(payload,step):
 print("TEAM",step,[x["id"] for x in payload["team"]])
 ids={x["id"] for x in payload["team"]}
 return {"success":{"coding-agent","security-agent","test-agent"}.issubset(ids),"risk":.05}

result=AdaptiveMultiAgentRuntime().run(
 "Fix OAuth security issue",agents,edges,executor,
 required_capabilities=["code","security","test"]
)
print("SUCCESS",result["success"])
