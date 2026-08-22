
from pathlib import Path
from compat.contract import ContractCompatibility
from e2e.torus_memory_path import TorusMemoryE2E
from faults.injector import FaultInjector
from install.doctor import doctor
from commercial.service import CommercialTopoSpaceService
from rc.version import VERSION

ROOT=Path(__file__).resolve().parents[1]

def test_version_is_rc(): assert VERSION.startswith("1.0.0-rc")
def test_response_backward_contract():
    s=CommercialTopoSpaceService()
    r=s.optimize({"objective":"x","context":[{"id":"a","tokens":10,"utility":1,"distance":.1,"score":.9,"drift":.1}]})
    assert ContractCompatibility().validate_response(r)["ok"]
def test_torus_e2e():
    x=TorusMemoryE2E().run();assert "auth-decision" in x["recalled"] and "auth-decision" in x["visible"]
def test_fault_injector_deterministic():
    f=FaultInjector(1);count=0
    for _ in range(100):
        try:f.maybe_fail(.1)
        except RuntimeError:count+=1
    assert 1<=count<=25
def test_install_doctor(): assert doctor(ROOT)["ok"]
def test_rc_console(): assert "customElements.define" in (ROOT/"web-sdk/rc-console.js").read_text()
