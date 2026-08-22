
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learned_field.network import CouplingFieldNetwork
from learned_field.models import FieldState

rng=random.Random(1729)
net=CouplingFieldNetwork()
before=[];after=[]

# Task family where memory->plan and tool->skill are beneficial.
for step in range(400):
    s=FieldState(hierarchy=rng.uniform(.6,1),tool_pressure=rng.uniform(.5,1),
                 memory_pressure=rng.uniform(.5,1),risk=rng.uniform(.2,.7))
    snap=net.forward(s)
    before.append((snap.couplings["memory"]["plan"],snap.couplings["tool"]["skill"]))
    net.update(s,{"memory":1.0,"plan":1.0,"tool":.9,"skill":.9})
    snap2=net.forward(s)
    after.append((snap2.couplings["memory"]["plan"],snap2.couplings["tool"]["skill"]))

out={
 "steps":400,
 "mean_memory_to_plan_before":statistics.mean(x[0] for x in before),
 "mean_memory_to_plan_after":statistics.mean(x[0] for x in after),
 "mean_tool_to_skill_before":statistics.mean(x[1] for x in before),
 "mean_tool_to_skill_after":statistics.mean(x[1] for x in after),
 "note":"Synthetic coupling-field learning regression; shows state-conditioned edge adaptation, not production agent quality."
}
print(json.dumps(out,indent=2))
assert out["mean_memory_to_plan_after"]>out["mean_memory_to_plan_before"]
assert out["mean_tool_to_skill_after"]>out["mean_tool_to_skill_before"]
Path("results/beta8_learned_field_benchmark.json").write_text(json.dumps(out,indent=2))
