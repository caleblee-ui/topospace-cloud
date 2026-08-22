
from pathlib import Path
import sys, json, random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning.topology_learner import TopologyLearner
from learning.multi_objective import MultiObjectiveTopologyLearner
from topology.drift import TopologicalDrift
from topology.persistence import zero_dim_persistence

def main():
    base=TopologyLearner(lr=.20,seed=11)
    learner=MultiObjectiveTopologyLearner(base)
    rewards=[]
    for i in range(30):
        cand=base.propose()
        # synthetic task family; good configs reduce latency/token/risk while succeeding
        p_err=abs(cand.p-1.6)/3
        e_err=abs(cand.epsilon-.28)
        success=max(0,min(1,1-(p_err+e_err)))
        metrics={
            "success":success,
            "token_cost_norm":min(1,.3+e_err),
            "latency_norm":min(1,.25+p_err),
            "tool_calls_norm":min(1,.2+e_err/2),
            "risk":min(1,.15+abs(cand.weights.get("risk",.4)-.55))
        }
        _,r=learner.update(cand,metrics);rewards.append(r)

    prev={"nodes":["task","auth","layout"],"edges":[("task","auth"),("task","layout")]}
    cur={"nodes":["task","auth","oauth","tests"],"edges":[("task","auth"),("auth","oauth"),("oauth","tests")]}
    drift=TopologicalDrift().compare(prev,cur)

    intervals=zero_dim_persistence(
        ["task","auth","oauth","layout"],
        [("task","auth",.10),("auth","oauth",.14),("task","layout",.70)]
    )
    finite=[x.persistence for x in intervals if x.persistence is not None]

    result={
        "episodes":len(rewards),
        "mean_reward":sum(rewards)/len(rewards),
        "last5_mean":sum(rewards[-5:])/5,
        "drift_score":drift.score,
        "entered":drift.entered,
        "exited":drift.exited,
        "persistence_finite":finite
    }
    print(json.dumps(result,indent=2))
    assert drift.score > .35
    assert any(x >= .70 for x in finite)
    Path("benchmarks/v07_topology_result.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__": main()
