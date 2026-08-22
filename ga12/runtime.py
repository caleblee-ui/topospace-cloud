from agent_gateway.gateway import AgentRuntimeGateway
from meta_runtime18.service import MetaPolicyProductionRuntime
from meta_runtime18.gateway_bridge import MetaPolicyGatewayBridge
from ga12.contracts import GADecisionContract
class TopoSpaceGA:
 def __init__(self):
  self.meta=MetaPolicyProductionRuntime();self.gateway=AgentRuntimeGateway();self.bridge=MetaPolicyGatewayBridge(self.meta)
 def optimize(self,req):
  d=self.bridge.apply(req,self.gateway.optimize(req))
  return GADecisionContract(d.model,d.diagnostics.get("meta_geometry",""),d.diagnostics.get("meta_path",""),d.token_budget)
