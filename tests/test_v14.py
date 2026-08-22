
from runtime.closed_loop import ClosedLoopTopoAgent
from runtime.decision_runtime import Candidate
from runtime.observation import AgentObservation

def test_observation_dict():
    o=AgentObservation(False,"x")
    d=o.to_dict()
    assert d["discovered_nodes"]==[] and d["success"] is False

def test_closed_loop_replans_and_succeeds():
    c=[Candidate("auth","code",.1,.8,.05),Candidate("tool","tool",.2,.4,.05)]
    e=[("tool","auth",.2)]
    def ex(payload,step):
        ids=[x["id"] for x in payload["context"]["code"]]
        return {"success":"test" in ids,"risk":.1}
    def mutate(cands,edges,obs,step):
        if not obs["success"] and not any(x.id=="test" for x in cands):
            cands=cands+[Candidate("test","code",.25,.7,.04)]
            edges=edges+[("auth","test",.1)]
        return cands,edges
    r=ClosedLoopTopoAgent(max_steps=3,drift_threshold=.1).run("fix bug",c,e,ex,mutate)
    assert r["success"] and len(r["steps"])==2
    assert r["steps"][0]["replanned"] is True
