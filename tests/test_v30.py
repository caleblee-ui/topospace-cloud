
from commercial.schemas import validate_optimize_request
from commercial.service import CommercialTopoSpaceService
from commercial.errors import TopoSpaceError
from commercial.health import HealthRegistry
from commercial.sla import SLATracker
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def test_request_contract(): assert validate_optimize_request({"objective":"x","context":[]})==[] and "objective_required" in validate_optimize_request({"context":[]})
def test_service_response_contract():
 r=CommercialTopoSpaceService().optimize({"objective":"x","context":[{"id":"a","tokens":10,"utility":1,"distance":.1,"score":.9,"drift":.1}]});assert r["api_version"]=="v1" and r["request_id"] and "result" in r
def test_invalid_request_error():
 try:CommercialTopoSpaceService().optimize({"context":[]})
 except TopoSpaceError as e: assert e.code=="INVALID_REQUEST" and e.status==400
 else: assert False
def test_health_registry():
 h=HealthRegistry();h.register("x",lambda:{"ok":True});assert h.snapshot()["ok"]
def test_sla_tracker():
 s=SLATracker();s.record(1);s.record(2);assert s.snapshot()["p95_ms"]>=1
def test_openapi_contract_exists(): assert "/v1/optimize" in json.loads((ROOT/"contracts/openapi-lite.json").read_text())["paths"]
