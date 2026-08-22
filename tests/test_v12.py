
from runtime.event_broker import EventBroker
from runtime.agent_graph_runtime import AgentGraphRuntime
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def test_event_broker():
    b=EventBroker();b.publish("w",{"seq":1});b.publish("w",{"seq":2})
    assert [x["seq"] for x in b.since("w",1)]==[2]

def test_agent_graph_runtime_lifecycle():
    r=AgentGraphRuntime("w")
    a=r.upsert_node("task",node_type="state",score=1)
    b=r.upsert_node("code",score=.8)
    c=r.connect("task","code",.2)
    assert c["seq"]==3 and len(c["payload"]["nodes"])==2 and len(c["payload"]["edges"])==1
    d=r.remove_node("code")
    assert len(d["payload"]["nodes"])==1 and not d["payload"]["edges"]

def test_live_web_assets():
    for p in ["web-sdk/topospace-live.js","web-sdk/topospace-graph-v1.2.js","studio-web/v1.2-live.html","api/server_v12.py"]:
        assert (ROOT/p).exists()
