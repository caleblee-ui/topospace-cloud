
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_router13.default_profiles import default_profiles
from model_router13.router import TopologyAwareModelRouter
from model_router13.models import RoutingContext

rng=random.Random(1203);r=TopologyAwareModelRouter(default_profiles())
counts={"fast":0,"balanced":0,"reasoning":0}
sensible=0
for i in range(5000):
    ctx=RoutingContext(
      risk=rng.random(),ambiguity=rng.random(),topology_complexity=rng.random(),
      coupling_strength=rng.random(),candidate_pressure=rng.random(),latency_pressure=rng.random(),
      expected_input_tokens=rng.randint(500,100000),expected_output_tokens=rng.randint(100,1500),
      expected_tool_calls=rng.randint(0,8)
    )
    out=r.route(ctx);m=out["selected"];counts[m]+=1
    hard=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity)>.8
    low=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity)<.3 and ctx.latency_pressure>.6
    if (hard and m in {"balanced","reasoning"}) or (low and m in {"fast","balanced"}) or (not hard and not low):
        sensible+=1

out={"runs":5000,"routes":counts,"heuristic_sensible_route_rate":sensible/5000,
     "note":"Synthetic topology-aware router regression. This measures routing behavior against coarse heuristics, not provider/model quality."}
print(json.dumps(out,indent=2))
assert all(counts.values())
assert out["heuristic_sensible_route_rate"]>.8
Path("results/beta12_topology_model_router_benchmark.json").write_text(json.dumps(out,indent=2))
