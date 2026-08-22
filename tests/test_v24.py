
import asyncio
from dataplane.backpressure import BackpressureController
from routing.provider_router import ProviderRouter,ProviderEndpoint
from routing.model_policy import ModelRoutingPolicy
from replication.snapshots import TopologySnapshotReplicator
from replication.leader import LeaderElection
from rollout.controller import RolloutController

def test_backpressure():
 b=BackpressureController(max_inflight=1,queue_threshold=1)
 assert b.admit()["ok"];assert b.admit()["queued"];assert not b.admit()["ok"];b.release()

def test_provider_router():
 e=[
  ProviderEndpoint("a","m1",100,1.0,.99,10000),
  ProviderEndpoint("b","m2",80,.5,.95,20000),
 ]
 r=ProviderRouter().select(e,5000)
 assert r.id in {"a","b"}

def test_model_tier():
 p=ModelRoutingPolicy()
 assert p.choose_tier(.1,.1,.9)=="small"
 assert p.choose_tier(.9,.9,.1)=="large"

def test_snapshot_replication():
 r=TopologySnapshotReplicator();x=r.publish("w",1,{"a":1})
 assert r.verify(x) and r.latest("w")["version"]==1

def test_leader_election():
 l=LeaderElection(lease_seconds=100)
 assert l.acquire("a") and not l.acquire("b") and l.current()=="a"

def test_rollout():
 r=RolloutController("v1");r.start_canary("v2",100)
 assert r.route("x")=="v2";r.rollback();assert r.route("x")=="v1"
