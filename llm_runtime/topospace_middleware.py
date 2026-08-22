
class TopoSpaceMiddleware:
    """
    Provider-neutral middleware. It reduces candidate context/tool/skill/plan
    spaces before the downstream model invocation and records actual provider usage.
    """
    def __init__(self,optimizer):
        self.optimizer=optimizer

    def optimize(self,request,spaces,state=None):
        return self.optimizer.optimize(
          request.task_id,
          request.metadata.get("objective","agent-task"),
          spaces,
          state or {}
        )

    def execute(self,provider,request,spaces,state=None,tools=None):
        optimized=self.optimize(request,spaces,state)
        live=optimized.get("live",optimized)
        bundle=live.get("bundle") or live.get("execution_bundle") or []
        result=provider.invoke(request,context=bundle,tools=tools)
        return {"optimization":optimized,"result":result}
