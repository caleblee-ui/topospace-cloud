
from pathlib import Path
import sys,json,tempfile,time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from trust.identity import ServiceIdentityIssuer,ServiceIdentity
from trust.attestation import PolicyAttestor
from release.sbom import SBOMBuilder
from release.signing import ReleaseSigner
from trust.integrity import RuntimeIntegrityVerifier
from compliance.export import ComplianceExporter

root=Path(__file__).resolve().parents[1]
issuer=ServiceIdentityIssuer("secret")
token=issuer.issue(ServiceIdentity("svc-a","tenant-a","topospace",time.time()+60,["runtime"]))
identity=issuer.verify(token,"topospace")

attestor=PolicyAttestor("attest")
att=attestor.attest("abc123","3.7.0-alpha","tenant-a")
att_ok=attestor.verify(att)

sbom=SBOMBuilder().build(root)
integrity=RuntimeIntegrityVerifier()
manifest=integrity.manifest(root)
integrity_ok=integrity.verify(root,manifest)

with tempfile.TemporaryDirectory() as d:
    p=Path(d)/"artifact.bin";p.write_bytes(b"topospace")
    signer=ReleaseSigner("release")
    signed=signer.sign_file(p)
    release_ok=signer.verify_file(p,signed)

bundle=ComplianceExporter().export(
 tenant_id="tenant-a",policies=[{"version":7}],audit_events=[],approvals=[],
 lineage=[],integrity=integrity_ok,metadata={"service_id":identity.service_id})

out={
 "service_identity":identity.service_id,
 "attestation_verified":att_ok,
 "release_signature_verified":release_ok,
 "runtime_integrity":integrity_ok["ok"],
 "sbom_components":len(sbom["components"]),
 "compliance_schema":bundle["schema"]
}
print(json.dumps(out,indent=2))
assert all([att_ok,release_ok,integrity_ok["ok"]]) and out["sbom_components"]>100
Path("results/v37_trust_benchmark.json").write_text(json.dumps(out,indent=2))
