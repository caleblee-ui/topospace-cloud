
from pathlib import Path
from runtime_sdk.middleware import TopoSpaceMiddleware
from runtime_sdk.adapter import AgentRuntimeAdapter
from runtime_sdk.decorators import instrument_tool
ROOT=Path(__file__).resolve().parents[1]
def test_lifecycle():
 m=TopoSpaceMiddleware();a=AgentRuntimeAdapter(m,"a")
 assert a.task_start("t")[0]["status"]=="started"
 a.before_model("t",prompt="x");a.after_model("t",answer="y");a.task_complete("t",True)
 assert m.tasks["t"]["success"] is True
def test_memory_hook():
 m=TopoSpaceMiddleware();a=AgentRuntimeAdapter(m,"a");a.task_start("t")
 m.cognitive.remember("m","auth",layer="semantic",importance=.9,confidence=.9,utility=.9,distance=.1)
 out=a.memory_recall("t",500)[0];assert out["memories"][0]["id"]=="m"
def test_tool_decorator():
 m=TopoSpaceMiddleware();a=AgentRuntimeAdapter(m,"a");a.task_start("t")
 @instrument_tool(a,"t","calc")
 def f(x):return x+1
 assert f(1)==2
def test_unknown_hook():
 m=TopoSpaceMiddleware()
 try:m.dispatch("nope","t")
 except ValueError:return
 assert False
def test_visual():
 assert "customElements.define" in (ROOT/"web-sdk/runtime-sdk-panel.js").read_text()
