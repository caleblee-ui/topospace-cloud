
from pathlib import Path
import tempfile,time
from trust.identity import ServiceIdentityIssuer,ServiceIdentity
from security.mtls import MTLSConfig
from trust.attestation import PolicyAttestor
from release.sbom import SBOMBuilder
from release.signing import ReleaseSigner
from trust.integrity import RuntimeIntegrityVerifier
from compliance.export import ComplianceExporter

ROOT=Path(__file__).resolve().parents[1]

def test_service_identity():
 i=ServiceIdentityIssuer("x");t=i.issue(ServiceIdentity("s","t","aud",time.time()+10,["r"]))
 assert i.verify(t,"aud").service_id=="s"

def test_mtls_validation():
 assert not MTLSConfig().validate()["ok"]
 assert MTLSConfig(enabled=False).validate()["ok"]

def test_attestation():
 a=PolicyAttestor("x");x=a.attest("h","v","t");assert a.verify(x)

def test_sbom():
 s=SBOMBuilder().build(ROOT);assert s["bomFormat"]=="CycloneDX" and s["components"]

def test_release_signing():
 with tempfile.TemporaryDirectory() as d:
  p=Path(d)/"x";p.write_text("a");s=ReleaseSigner("k");b=s.sign_file(p);assert s.verify_file(p,b)

def test_integrity():
 v=RuntimeIntegrityVerifier();m=v.manifest(ROOT);assert v.verify(ROOT,m)["ok"]

def test_compliance_export():
 c=ComplianceExporter().export(tenant_id="t",policies=[],audit_events=[],approvals=[],lineage=[],integrity={"ok":True})
 assert c["schema"]=="topospace-compliance-v1"

def test_trust_visual():
 assert "customElements.define" in (ROOT/"web-sdk/trust-panel.js").read_text()
