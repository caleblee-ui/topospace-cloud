
from optimization.minimal_team import MinimalTeamOptimizer
from optimization.token_optimizer import TokenBudgetController,TokenBudget
from optimization.context_pruner import TopologicalContextPruner
from telemetry.efficiency import RunMetrics,compare

def test_minimal_team():
 m=[
  {"id":"code","capabilities":["code"],"score":.9,"reliability":1,"cost":.1,"risk":.05},
  {"id":"test","capabilities":["test"],"score":.8,"reliability":1,"cost":.1,"risk":.05},
  {"id":"decoy","capabilities":["front"],"score":.1,"reliability":1,"cost":.1,"risk":.1},
 ]
 o=MinimalTeamOptimizer().optimize(m,["code","test"],.2)
 assert [x["id"] for x in o]==["code","test"]

def test_token_budget():
 items=[{"id":"a","tokens":60,"utility":.9},{"id":"b","tokens":60,"utility":.1}]
 o=TokenBudgetController(TokenBudget(100,20)).prune(items)
 assert o["tokens"]<=80 and o["kept"][0]["id"]=="a"

def test_context_pruner():
 o=TopologicalContextPruner().prune([{"id":"a","distance":.1,"score":.8,"drift":.1},{"id":"b","distance":.8,"score":.9,"drift":.1}],.3)
 assert [x["id"] for x in o["kept"]]==["a"]

def test_efficiency_compare():
 b=RunMetrics(1000,100,10,4,1000,1,True);o=RunMetrics(600,100,6,3,700,.7,True)
 r=compare(b,o)
 assert r["token_reduction_pct"]>30 and r["success_delta_pp"]==0
