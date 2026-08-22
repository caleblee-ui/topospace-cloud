
from pathlib import Path
import sys,random,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from model_router13.default_profiles import default_profiles
from model_router13.models import RoutingContext
from routing_policy14.policy import LearnedModelRoutingPolicy
from routing_policy14.models import RoutingOutcome
from routing_policy14.features import topology_bucket
rng=random.Random(1204);p=LearnedModelRoutingPolicy(default_profiles())
truth={"low":"fast","medium":"balanced","high":"reasoning"}
contexts=[]
for _ in range(3000):
    # Deliberately create coverage across all three topology classes.
    cls=rng.choice(["low","medium","high"])
    if cls=="low":
        c=RoutingContext(risk=rng.uniform(0,.25),ambiguity=rng.uniform(0,.25),topology_complexity=rng.uniform(0,.25),
                         coupling_strength=rng.uniform(0,.25),expected_tool_calls=rng.randint(0,2),expected_input_tokens=rng.randint(500,30000))
    elif cls=="medium":
        c=RoutingContext(risk=rng.uniform(.35,.65),ambiguity=rng.uniform(.35,.65),topology_complexity=rng.uniform(.35,.65),
                         coupling_strength=rng.uniform(.2,.6),expected_tool_calls=rng.randint(1,5),expected_input_tokens=rng.randint(500,30000))
    else:
        c=RoutingContext(risk=rng.uniform(.8,1),ambiguity=rng.uniform(.6,1),topology_complexity=rng.uniform(.75,1),
                         coupling_strength=rng.uniform(.5,1),expected_tool_calls=rng.randint(3,8),expected_input_tokens=rng.randint(500,30000))
    contexts.append(c)
pre=sum(p.route(c)["selected"]==truth[topology_bucket(c)] for c in contexts)/len(contexts)
quality={
 ("low","fast"):.97,("low","balanced"):.72,("low","reasoning"):.68,
 ("medium","fast"):.66,("medium","balanced"):.97,("medium","reasoning"):.80,
 ("high","fast"):.50,("high","balanced"):.72,("high","reasoning"):.99,
}
lat={"fast":280,"balanced":650,"reasoning":1250};cost={"fast":.04,"balanced":.18,"reasoning":.65}
for b in ("low","medium","high"):
    for m in ("fast","balanced","reasoning"):
        for _ in range(300):
            q=max(0,min(1,quality[(b,m)]+rng.uniform(-.02,.02)))
            p.feedback(RoutingOutcome(m,q,1200,250,lat[m]+rng.uniform(-40,40),cost[m]+rng.uniform(0,.01),True,b))
post=sum(p.route(c)["selected"]==truth[topology_bucket(c)] for c in contexts)/len(contexts)
out={"contexts":len(contexts),"pre_learning_match_rate":pre,"post_learning_match_rate":post,
     "improvement_points":100*(post-pre),
     "note":"Constructed synthetic regression benchmark; validates topology-conditioned learning, not live provider superiority."}
print(json.dumps(out,indent=2))
assert post>pre and post>.95
Path("results/beta12_learned_routing_policy_benchmark.json").write_text(json.dumps(out,indent=2))
