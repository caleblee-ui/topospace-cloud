
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from geometry_policy.model import PolicyState
from geometry_policy.network import GeometryPolicyNetwork

p=GeometryPolicyNetwork()
scenarios={
 "exploratory":PolicyState(ambiguity=1.0),
 "security_critical":PolicyState(risk=1.0),
 "hierarchical_workspace":PolicyState(hierarchy=1.0),
 "candidate_overload":PolicyState(candidate_pressure=1.0),
}
out={}
for name,s in scenarios.items():
 d=p.decide(s)
 out[name]={"aggregator":d.aggregator,"p":d.p,"epsilon":d.epsilon,
            "confidence":d.confidence,"probabilities":d.scores}
print(json.dumps(out,indent=2))
assert out["security_critical"]["aggregator"] in {"chebyshev","nested"}
assert out["hierarchical_workspace"]["aggregator"]=="nested"
assert len(set(x["aggregator"] for x in out.values()))>=3
Path("results/beta5_policy_benchmark.json").write_text(json.dumps(out,indent=2))
