
from pathlib import Path
import sys, json, random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learning.topology_learner import TopologyLearner, TopologyParams
from runtime.replanner import ReplanningLoop

def score(params, target):
    # synthetic operational objective used only as regression harness
    wp=params.weights
    err=(params.p-target["p"])**2 + 2*(params.epsilon-target["epsilon"])**2
    for k,v in target["weights"].items():
        err += 0.3*(wp.get(k,0)-v)**2
    return max(-1.0, 1.0-err)

def main():
    learner=TopologyLearner(lr=.25, seed=13)
    target={"p":1.5,"epsilon":.27,"weights":{"path":1.5,"symbol":1.6,"semantic":.65}}
    rewards=[]
    for episode in range(35):
        loop=ReplanningLoop(learner,max_steps=3)
        def attempt(params,step):
            r=score(params,target)
            return {"success": r>.86, "reward":r, "episode":episode}
        out=loop.run(attempt)
        rewards.append(out["best"]["reward"])
    result={
      "episodes":len(rewards),
      "first5_mean":sum(rewards[:5])/5,
      "last5_mean":sum(rewards[-5:])/5,
      "final_params":learner.state_dict()["params"]
    }
    print(json.dumps(result,indent=2))
    assert result["last5_mean"] >= result["first5_mean"]
    Path("benchmarks/learning_replanning_result.json").write_text(json.dumps(result,indent=2))
if __name__=="__main__": main()
