
from __future__ import annotations
from production.adaptive_engine import AdaptiveTopoSpaceEngine
from dataplane.backpressure import BackpressureController
from routing.provider_router import ProviderRouter
from routing.model_policy import ModelRoutingPolicy
from replication.snapshots import TopologySnapshotReplicator
from rollout.controller import RolloutController

class TopoSpaceDataPlane:
    def __init__(self,engine=None):
        self.engine=engine or AdaptiveTopoSpaceEngine()
        self.backpressure=BackpressureController()
        self.provider_router=ProviderRouter()
        self.model_policy=ModelRoutingPolicy()
        self.snapshots=TopologySnapshotReplicator()
        self.rollout=RolloutController("stable")

    def optimize_and_route(self,request,endpoints=None):
        admit=self.backpressure.admit()
        if not admit["ok"]:return {"error":"overloaded"}
        try:
            plan=self.engine.optimize_adaptive(**request)
            tier=self.model_policy.choose_tier(
                request.get("complexity",.5),request.get("uncertainty",.3),request.get("cost_pressure",.5))
            provider=None
            if endpoints:
                provider=self.provider_router.select(endpoints,plan.get("context_tokens",0))
            return {"plan":plan,"model_tier":tier,"provider":getattr(provider,"id",None)}
        finally:
            self.backpressure.release()
