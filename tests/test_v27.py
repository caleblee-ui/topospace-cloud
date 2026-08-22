
from pathlib import Path
from middleware.hooks import AgentEnvelope
from middleware.topospace_middleware import TopoSpaceMiddleware
from runtime.generic_agent_loop import GenericAgentLoop
from runtime.middleware_trace import MiddlewareTrace
from torusdb.memory_backend import InMemoryTorusBackend
from torusdb.models import MemoryRecord
from torusdb.bridge import TorusTopoMemoryBridge

ROOT=Path(__file__).resolve().parents[1]

def test_framework_agnostic_inference_hook():
    m=TopoSpaceMiddleware()
    env=AgentEnvelope("fix auth",context=[
      {"id":"auth","tokens":100,"utility":1,"distance":.1,"score":.9,"drift":.05},
      {"id":"noise","tokens":100,"utility":.1,"distance":.8,"score":.1,"drift":.7},
    ])
    loop=GenericAgentLoop(m,lambda e:{"visible":[x["id"] for x in e.context]})
    out=loop.run(env)
    assert out["success"] and out["result"]["visible"]==["auth"]

def test_torus_memory_recall_hook():
    b=InMemoryTorusBackend()
    b.upsert(MemoryRecord("m1","oauth decision",semantic_score=.9,importance=.9,distance=.1,tokens=80))
    m=TopoSpaceMiddleware(memory_bridge=TorusTopoMemoryBridge(b))
    env=AgentEnvelope("oauth")
    r=m.memory_recall(env,"oauth")
    assert r.payload and r.payload[0]["id"]=="m1"

def test_state_update_feedback():
    m=TopoSpaceMiddleware();env=AgentEnvelope("x",uncertainty=.2)
    m.state_update(env,{"type":"failure","uncertainty":.8,"drift":.3})
    assert env.previous_success is False and env.uncertainty>=.8 and env.drift>=.3

def test_trace():
    t=MiddlewareTrace();t.add("before_inference",x=1)
    assert t.export()[0]["phase"]=="before_inference"

def test_visualization_asset():
    js=(ROOT/"web-sdk/middleware-flow.js").read_text()
    html=(ROOT/"studio-web/v2.7-middleware.html").read_text()
    assert "customElements.define" in js and "TopoSpaceMiddlewareFlowSDK.mount" in html
