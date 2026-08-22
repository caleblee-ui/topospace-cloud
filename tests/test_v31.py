
from pathlib import Path
import tempfile,time
from customer.metering import UsageMeter
from customer.license import License,LicenseManager
from customer.backup import BackupManager
from customer.oidc import OIDCVerifier
from migrations.runner import MigrationRunner,Migration
from admin.service import AdminService
from customer.service import CustomerTopoSpaceService

ROOT=Path(__file__).resolve().parents[1]

def test_metering():
    m=UsageMeter();m.record("t","requests",2);assert m.total("t","requests")==2

def test_license():
    m=LicenseManager("s");tok=m.issue(License("c","enterprise",time.time()+100))
    assert m.verify(tok).customer_id=="c"

def test_backup():
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"x.txt";p.write_text("hello")
        b=Path(d)/"b.tar.gz"
        mgr=BackupManager();manifest=mgr.create(b,[p]);assert manifest["files"][0]["size"]==5
        assert mgr.inspect(b)["files"][0]["name"]=="x.txt"

def test_migration():
    seen=[];r=MigrationRunner();r.register(Migration(1,"a",lambda c:seen.append("a")));r.register(Migration(2,"b",lambda c:seen.append("b")))
    out=r.migrate();assert [x["version"] for x in out]==[1,2] and seen==["a","b"]

def test_admin():
    a=AdminService();a.create_tenant("t");assert a.disable_tenant("t")["enabled"] is False

def test_customer_service_metering():
    s=CustomerTopoSpaceService()
    r=s.optimize({"objective":"x","context":[{"id":"a","tokens":10,"utility":1,"distance":.1,"score":.9,"drift":.1}]},"t","p")
    assert s.meter.total("t","optimization_requests")==1

def test_helm_chart_exists():
    assert (ROOT/"deploy/helm/topospace/Chart.yaml").exists()
    assert (ROOT/"deploy/terraform/main.tf").exists()
