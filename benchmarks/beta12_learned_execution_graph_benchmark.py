
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from learned_graph16.templates import default_path_templates
from learned_graph16.policy import LearnedExecutionGraphPolicy
from learned_graph16.models import PathOutcome
from learned_graph16.bucket import graph_topology_bucket
from model_router13.models import RoutingContext

rng=random.Random(1206);p=LearnedExecutionGraphPolicy(default_path_templates())
truth={"low":"fast_only","medium":"balanced_tool","high":"memory_balanced_reasoning"}

contexts=[]
for _ in range(3000):
    cls=rng.choice(["low","medium","high"])
    if cls=="low":
        c=RoutingContext(risk=rng.uniform(0,.25),ambiguity=rng.uniform(0,.25),topology_complexity=rng.uniform(0,.25),
                         coupling_strength=rng.uniform(0,.25),expected_tool_calls=rng.randint(0,2))
    elif cls=="medium":
        c=RoutingContext(risk=rng.uniform(.35,.65),ambiguity=rng.uniform(.35,.65),topology_complexity=rng.uniform(.35,.65),
                         coupling_strength=rng.uniform(.25,.6),expected_tool_calls=rng.randint(2,5))
    else:
        c=RoutingContext(risk=rng.uniform(.8,1),ambiguity=rng.uniform(.65,1),topology_complexity=rng.uniform(.75,1),
                         coupling_strength=rng.uniform(.5,1),expected_tool_calls=rng.randint(3,8))
    contexts.append(c)

pre=sum(p.route(c)["selected"]==truth[graph_topology_bucket(c)] for c in contexts)/len(contexts)

templates={x.name:x for x in default_path_templates()}
for bucket in ("low","medium","high"):
    for path in templates.values():
        for _ in range(250):
            good=path.name==truth[bucket]
            reward=(.97 if good else .62)+rng.uniform(-.025,.025)
            success=good or rng.random()<.65
            cost=path.nominal_cost*rng.uniform(.9,1.1)
            lat=path.nominal_latency_ms*rng.uniform(.9,1.1)
            p.feedback(PathOutcome(bucket,path.name,reward,success,cost,lat))

post=sum(p.route(c)["selected"]==truth[graph_topology_bucket(c)] for c in contexts)/len(contexts)

out={
 "contexts":len(contexts),
 "pre_learning_match_rate":pre,
 "post_learning_match_rate":post,
 "improvement_points":100*(post-pre),
 "note":"Constructed execution-path ground truth for regression only; not live provider/task quality evidence."
}
print(json.dumps(out,indent=2))
assert post>pre and post>.95
Path("results/beta12_learned_execution_graph_benchmark.json").write_text(json.dumps(out,indent=2))
