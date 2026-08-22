
from runtime.decision_runtime import TopoDecisionRuntime,Candidate
from runtime.context_budget import ContextBudgetManager
from runtime.memory_policy import MemoryRetentionPolicy
from agent.topological_agent import TopologicalAgentRuntime

def fixture():
 c=[
  Candidate("auth","code",.1,.8,.05),
  Candidate("test","code",.3,.7,.05),
  Candidate("decoy","code",.11,.04,.6),
  Candidate("grep","tool",.2,.4,.05)
 ]
 e=[("auth","test",.1),("auth","decoy",.8),("grep","auth",.2)]
 return c,e

def test_decision_runtime():
 c,e=fixture();d=TopoDecisionRuntime().select(c,e,2,["code"])
 assert [x["id"] for x in d.selected]==["auth","test"]

def test_budget_policy():
 b=ContextBudgetManager().budgets("fix bug and test")
 assert b["code"]>=8 and b["tool"]>=4

def test_memory_policy():
 rows=[{"id":"a","score":.9},{"id":"b","score":.2}]
 o=MemoryRetentionPolicy().decide(rows,.5)
 assert [x["id"] for x in o["keep"]]==["a"] and [x["id"] for x in o["evict"]]==["b"]

def test_agent_runtime_controls_context():
 c,e=fixture();seen={}
 def ex(payload):
  seen.update(payload["context"]);return {"success":True}
 a=TopologicalAgentRuntime();r=a.step("fix bug",c,e,ex)
 assert r.success and seen["code"][0]["id"]=="auth"
