
from pathlib import Path
import sys,random,json,statistics
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from llm_runtime.contracts import LLMUsage
from experiments.ab_runner import ABAgentExperiment

rng=random.Random(1201);exp=ABAgentExperiment()
for i in range(1000):
    base_in=rng.randint(1800,6500)
    base_out=rng.randint(150,900)
    base_tools=rng.randint(2,8)
    reduction=rng.uniform(.25,.58)
    topo_in=int(base_in*(1-reduction))
    topo_out=int(base_out*rng.uniform(.96,1.04))
    topo_tools=max(1,int(base_tools*rng.uniform(.45,.85)))
    q=rng.uniform(.78,.96)
    exp.record(
      str(i),
      LLMUsage(base_in,base_out,base_tools,rng.uniform(700,2200),True),
      LLMUsage(topo_in,topo_out,topo_tools,rng.uniform(500,1700),True),
      q,q+rng.uniform(-.01,.02)
    )
out=exp.summary()
out["note"]="Synthetic provider-usage A/B harness. Validates measurement pipeline only; live model/API experiments are required for marketing claims."
print(json.dumps(out,indent=2))
assert out["mean_input_token_saving_pct"]>25
assert out["mean_quality_delta"]>-0.01
Path("results/beta12_provider_ab_harness.json").write_text(json.dumps(out,indent=2))
