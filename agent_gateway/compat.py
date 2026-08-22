
class OpenAICompatibleGateway:
    """
    Compatibility helper: accepts an OpenAI-style request dictionary and returns
    TopoSpace routing metadata without requiring application framework changes.
    """
    def __init__(self,gateway):self.gateway=gateway
    def optimize_payload(self,payload,spaces=None,state=None):
        from agent_gateway.contracts import GatewayRequest
        spaces=spaces or {}
        req=GatewayRequest(
          task_id=str(payload.get("metadata",{}).get("task_id","request")),
          messages=list(payload.get("messages",[])),
          model=payload.get("model","auto"),
          max_tokens=int(payload.get("max_tokens",1024)),
          tools=list(spaces.get("tool",payload.get("tools",[]))),
          memory=list(spaces.get("memory",[])),
          skills=list(spaces.get("skill",[])),
          plans=list(spaces.get("plan",[])),
          state=state or {},
          metadata=dict(payload.get("metadata",{}))
        )
        return self.gateway.optimize(req)
