
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from joint_optimizer.controller import JointGeometryController
from joint_optimizer.stability import GeometryStabilityMonitor
from unified_runtime.models import AgentState

rng=random.Random(1729)
ctrl=JointGeometryController();stability=GeometryStabilityMonitor()
joint_scores=[];field_gains=[];instabilities=[]

for step in range(500):
    state=AgentState(
      f"t{step}","task",
      risk=rng.uniform(.2,.9),
      ambiguity=rng.uniform(.1,.9),
      hierarchy=rng.uniform(.2,1.0),
      candidate_pressure=rng.random(),
      latency_pressure=rng.random(),
      metadata={"memory_pressure":rng.random(),"tool_pressure":rng.random()}
    )
    before=ctrl.decide(state)
    mem_plan_before=before["field"].couplings["memory"]["plan"]

    rewards={"memory":1.0,"plan":1.0,"tool":.85,"skill":.85}
    joint_reward=.9
    ctrl.update(before,rewards,joint_reward)

    after=ctrl.decide(state)
    mem_plan_after=after["field"].couplings["memory"]["plan"]
    field_gains.append(mem_plan_after-mem_plan_before)
    instabilities.append(stability.distance(before,after))
    joint_scores.append(after["joint"].aggregate_score)

out={
  "steps":500,
  "mean_memory_to_plan_gain":statistics.mean(field_gains),
  "mean_joint_confidence":statistics.mean(joint_scores),
  "mean_update_instability":statistics.mean(instabilities),
  "note":"Synthetic joint-learning regression; demonstrates coordinated A_theta + C_theta updates, not production task quality."
}
print(json.dumps(out,indent=2))
assert out["mean_memory_to_plan_gain"]>0
assert out["mean_update_instability"]<.2
Path("results/beta9_joint_optimizer_benchmark.json").write_text(json.dumps(out,indent=2))
