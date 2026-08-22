
from pathlib import Path
from console.operations import OperationsStore
from console.observed_service import ObservedCustomerService

ROOT=Path(__file__).resolve().parents[1]

def test_operations_topology():
 o=OperationsStore();o.record("optimization","t",request_id="r1",objective="x",selected_context=[{"id":"m1","type":"memory","score":.9}])
 g=o.topology("t");assert len(g["nodes"])==2 and g["edges"][0]["target"]=="m1"

def test_observed_service():
 s=ObservedCustomerService()
 s.optimize({"objective":"x","context":[{"id":"a","tokens":10,"utility":1,"distance":.1,"score":.9,"drift":.1}]},"t","p")
 assert s.operations.recent("t")[-1]["type"]=="optimization"

def test_console_assets():
 js=(ROOT/"web-sdk/admin-console.js").read_text()
 html=(ROOT/"studio-web/v3.2-admin-console.html").read_text()
 assert "customElements.define" in js and "TopoSpaceAdminConsoleSDK.mount" in html
