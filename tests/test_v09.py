
from runtime.hybrid_context import HybridTopologicalScorer
from runtime.web_graph_payload import build_graph_payload
def test_hybrid_promotes_stable_structural_context():
 s=HybridTopologicalScorer();nodes=["auth","test","decoy"];edges=[("auth","test",.1),("auth","decoy",.8)]
 dist={"auth":.1,"test":.3,"decoy":.11};pers={"auth":.8,"test":.7,"decoy":.05};drift={"auth":.05,"test":.05,"decoy":.5}
 assert [x["id"] for x in s.score(nodes,edges,dist,pers,drift)[:2]]==["auth","test"]
def test_web_payload():
 p=build_graph_payload(["a","b"],[("a","b",.2)],[{"id":"a","score":.9,"components":{"adaptive":1},"topological_support":.8}])
 assert len(p["nodes"])==2 and p["edges"][0]["affinity"]==.8
