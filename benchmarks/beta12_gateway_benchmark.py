
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from agent_gateway.context import ContextBudgeter
from agent_gateway.model_router import ModelRouter

rng=random.Random(1202);b=ContextBudgeter();r=ModelRouter()
base=[];budgets=[];routes={"reasoning":0,"fast":0,"balanced":0}
for i in range(5000):
    max_tokens=rng.randint(512,8192);cp=rng.random();lp=rng.random();risk=rng.random();amb=rng.random()
    base.append(max_tokens);budgets.append(b.budget(max_tokens,cp,lp))
    routes[r.route("auto",{"risk":risk,"ambiguity":amb,"latency_pressure":lp})]+=1
out={
 "runs":5000,
 "mean_requested_budget":statistics.mean(base),
 "mean_gateway_budget":statistics.mean(budgets),
 "budget_reduction_pct":100*(1-statistics.mean(budgets)/statistics.mean(base)),
 "logical_model_routes":routes,
 "note":"Synthetic gateway control-plane benchmark; budget reduction is an assigned generation budget, not measured provider token billing."
}
print(json.dumps(out,indent=2))
assert out["budget_reduction_pct"]>10
assert all(routes.values())
Path("results/beta12_gateway_benchmark.json").write_text(json.dumps(out,indent=2))
