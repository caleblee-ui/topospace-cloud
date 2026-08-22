
from pathlib import Path
from ga.version import VERSION,STATUS
from config.production import ProductionEnvironment
from contracts.deprecation import DeprecationPolicy
from e2e.torus_http_smoke import run_http_e2e
from release.manifest import build_release_manifest

ROOT=Path(__file__).resolve().parents[1]

def test_ga_version():
    assert VERSION.startswith(("1.0.","1.1.","1.2.","1.3.")) and STATUS in {"ALPHA","BETA","GA"}

def test_environment_validation():
    assert ProductionEnvironment(port=8787).validate()["ok"]

def test_deprecation_policy():
    p=DeprecationPolicy()
    assert not p.validate_change(True,30,"v1")["ok"]
    assert p.validate_change(True,180,"v2")["ok"]

def test_torus_http_e2e():
    assert run_http_e2e()["ok"]

def test_release_manifest():
    m=build_release_manifest(ROOT,VERSION)
    assert m["status"]=="GA" and len(m["files"])>100

def test_docker_assets():
    assert (ROOT/"deploy/docker/Dockerfile").exists()
    assert (ROOT/"deploy/compose/docker-compose.yml").exists()

def test_ga_console():
    assert "customElements.define" in (ROOT/"web-sdk/ga-console.js").read_text()
