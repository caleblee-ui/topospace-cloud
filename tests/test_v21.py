
from pathlib import Path
import tempfile
from production.auth import APIKeyManager
from production.config_store import ConfigStore
from production.config import ProductionConfig
from state.checkpoint import CheckpointStore
from production.concurrent_engine import ConcurrentTopoSpaceEngine

def test_api_keys():
 a=APIKeyManager();k=a.create("x");assert a.verify("x",k["secret"]);a.disable("x");assert not a.verify("x",k["secret"])

def test_config_store_versioning():
 with tempfile.TemporaryDirectory() as d:
  s=ConfigStore(Path(d)/"c.db");v=s.put("w",ProductionConfig());assert v==1
  assert s.get("w")["version"]==1

def test_checkpoint_recovery():
 with tempfile.TemporaryDirectory() as d:
  s=CheckpointStore(Path(d)/"s.db");s.save("w","r",1,{"x":1});assert s.latest("w","r")["payload"]["x"]==1

def test_concurrent_engine():
 e=ConcurrentTopoSpaceEngine(max_workers=2)
 c=[{"id":"a","tokens":100,"utility":1,"distance":.1,"score":.9,"drift":.1}]
 f=e.submit("x",c,[],[],uncertainty=.2)
 assert f.result()["context"]
 e.shutdown()
