
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from optimization.context_pruner import TopologicalContextPruner
from optimization.token_optimizer import TokenBudgetController,TokenBudget
from optimization.minimal_team import MinimalTeamOptimizer
from telemetry.efficiency import RunMetrics,compare

def main():
    # Synthetic deterministic fixture. NOT a marketing performance claim.
    context=[
      {"id":"task","tokens":900,"utility":1.0,"distance":0.0,"score":1.0,"drift":0},
      {"id":"auth","tokens":5200,"utility":.95,"distance":.10,"score":.94,"drift":.05},
      {"id":"oauth","tokens":4800,"utility":.90,"distance":.14,"score":.88,"drift":.08},
      {"id":"tests","tokens":4100,"utility":.82,"distance":.22,"score":.80,"drift":.05},
      {"id":"logs","tokens":7600,"utility":.45,"distance":.31,"score":.48,"drift":.20},
      {"id":"frontend","tokens":6800,"utility":.10,"distance":.72,"score":.14,"drift":.55},
      {"id":"history-old","tokens":9300,"utility":.08,"distance":.81,"score":.12,"drift":.70},
    ]
    p=TopologicalContextPruner().prune(context,epsilon=.35,min_score=.25,max_drift=.45)
    budget=TokenBudgetController(TokenBudget(max_input_tokens=24000,reserve_output_tokens=3000)).prune(p["kept"])

    team=[
      {"id":"coding","capabilities":["code"],"score":.94,"reliability":.96,"cost":.2,"risk":.08},
      {"id":"security","capabilities":["security"],"score":.90,"reliability":.97,"cost":.2,"risk":.05},
      {"id":"test","capabilities":["test"],"score":.86,"reliability":.96,"cost":.18,"risk":.05},
      {"id":"frontend","capabilities":["frontend"],"score":.18,"reliability":.90,"cost":.15,"risk":.10},
    ]
    minimal=MinimalTeamOptimizer().optimize(team,["code","security","test"],min_marginal_utility=.25)
    base_tokens=sum(x["tokens"] for x in context)+4500
    opt_tokens=budget["tokens"]+3600
    base=RunMetrics(base_tokens,2200,8,4,12000,.52,True)
    opt=RunMetrics(opt_tokens,1800,5,len(minimal),8500,.34,True)
    result=compare(base,opt)
    result["context_kept"]=[x["id"] for x in budget["kept"]]
    result["team"]=[x["id"] for x in minimal]
    result["fixture"]="synthetic deterministic; external benchmark required before marketing claim"
    print(json.dumps(result,indent=2))
    assert result["token_reduction_pct"]>30
    assert result["success_delta_pp"]==0
    assert result["team"]==["coding","security","test"]
    Path("benchmarks/v16_efficiency_result.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__":main()
