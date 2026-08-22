
from pathlib import Path
import tempfile
from learning.topology_learner import TopologyLearner
from runtime.replanner import ReplanningLoop
from runtime.live_trace import LiveTraceBuffer
from sandbox.executor import PatchSandbox

def test_learner_and_replanner():
    l=TopologyLearner(seed=1)
    before=l.params.p
    loop=ReplanningLoop(l,max_steps=2)
    result=loop.run(lambda p,s: {"success": s==1, "reward": 1 if s==1 else -.5})
    assert len(result["trace"])==2
    assert len(l.history)==2

def test_live_trace():
    b=LiveTraceBuffer()
    f=b.push("context","s1",[{"id":"a"}],[],{"epsilon":.2})
    assert f["seq"]==1 and b.since(0)[0]["state_id"]=="s1"

def test_patch_sandbox():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d); (p/"x.txt").write_text("a")
        with PatchSandbox(p) as s:
            (s.copy/"x.txt").write_text("b")
            r=s.run(["python","-c","print(open('x.txt').read())"])
            assert r.returncode==0 and "b" in r.stdout
        assert (p/"x.txt").read_text()=="a"
