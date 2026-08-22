
from agent_gateway.context import ContextBudgeter
from agent_gateway.model_router import ModelRouter
from agent_gateway.cache import SemanticDecisionCache
from agent_gateway.spaces import request_spaces
from runtime_server.joint_service import JointRuntimeService
from agent_gateway.contracts import GatewayDecision

class AgentRuntimeGateway:
    """
    Drop-in optimization control plane:
    context -> memory/tool/skill/plan topology -> model route -> budget -> telemetry.
    """
    def __init__(self,service=None,topology_model_router=None):
        self.service=service or JointRuntimeService()
        self.models=ModelRouter();self.budgeter=ContextBudgeter()
        self.cache=SemanticDecisionCache()
        self.topology_model_router=topology_model_router

    def optimize(self,req):
        key=self.cache.key(req);cached=self.cache.get(key)
        if cached:return cached
        spaces=request_spaces(req)
        out=self.service.optimize(req.task_id,req.metadata.get("objective","agent-task"),spaces,req.state)
        live=out["live"]
        routes=live.get("routes",{})
        ids=lambda d:[x["id"] for x in routes.get(d,{}).get("selected",[])]
        model=self.models.route(req.model,req.state)
        budget=self.budgeter.budget(req.max_tokens,float(req.state.get("candidate_pressure",0)),float(req.state.get("latency_pressure",0)))
        decision=GatewayDecision(model,budget,ids("memory"),ids("tool"),ids("skill"),ids("plan"),{
          "geometry":live.get("geometry",{}),
          "joint_iterations":getattr(live.get("joint_state"),"iteration",None)
        })
        if self.topology_model_router is not None and req.model=="auto":
            decision=self.topology_model_router.apply(req,decision)
        self.cache.put(key,decision)
        return decision
