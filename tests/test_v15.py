
from multiagent.models import AgentNode
from multiagent.team_builder import TopologicalTeamBuilder
from multiagent.orchestrator import AdaptiveMultiAgentRuntime
from runtime.agent_team_graph import team_to_graph_payload

def fixture():
 agents=[
  AgentNode("code",["code"],.1,.8,.05),
  AgentNode("security",["security"],.2,.7,.05),
  AgentNode("test",["test"],.24,.7,.04),
  AgentNode("decoy",["frontend"],.11,.03,.6),
 ]
 edges=[("code","security",.1),("code","test",.12),("code","decoy",.8),("security","test",.15)]
 return agents,edges

def test_team_builder_covers_capabilities():
 a,e=fixture()
 t=TopologicalTeamBuilder().build("secure code",a,e,max_agents=3,required_capabilities=["code","security","test"])
 ids={x["id"] for x in t.members}
 assert {"code","security","test"}.issubset(ids)

def test_multiagent_runtime():
 a,e=fixture()
 def ex(payload,step):
  ids={x["id"] for x in payload["team"]}
  return {"success":{"code","security","test"}.issubset(ids),"risk":.05}
 r=AdaptiveMultiAgentRuntime(max_steps=2).run("secure code",a,e,ex,required_capabilities=["code","security","test"])
 assert r["success"]

def test_team_graph_payload():
 a,e=fixture()
 t=TopologicalTeamBuilder().build("secure code",a,e,max_agents=3,required_capabilities=["code","security","test"])
 p=team_to_graph_payload("secure code",t,1)
 assert p["nodes"][0]["type"]=="state"
 assert any(x["type"]=="agent" for x in p["nodes"])
 assert any(x["type"]=="collaboration" for x in p["edges"])
