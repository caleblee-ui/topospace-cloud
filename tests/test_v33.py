
from pathlib import Path
from autopilot.controller import TopologyAutopilot
from autopilot.models import RuntimeSignals
from autopilot.runtime import AutopilotRuntime
from autopilot.service import AutopilotTopoSpaceService

ROOT=Path(__file__).resolve().parents[1]

def test_autopilot_expands_on_degradation():
 a=TopologyAutopilot()
 good=a.decide(RuntimeSignals(.98,.1,.05,.8,.5,0,.9))
 bad=a.decide(RuntimeSignals(.6,.85,.6,.3,.3,.4,.3))
 assert bad.epsilon>good.epsilon and bad.max_context_tokens>good.max_context_tokens and bad.memory_recall_limit>good.memory_recall_limit

def test_runtime_history():
 r=AutopilotRuntime();r.update(RuntimeSignals());assert len(r.recent())==1

def test_service_autopilot():
 s=AutopilotTopoSpaceService()
 out=s.optimize_with_autopilot({"objective":"x","context":[{"id":"a","tokens":10,"utility":1,"distance":.1,"score":.9,"drift":.1}]})
 assert "autopilot" in out and "memory_recall_limit" in out["result"]["adaptive"]

def test_visual_asset():
 js=(ROOT/"web-sdk/autopilot-panel.js").read_text()
 assert "customElements.define" in js
