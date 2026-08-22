
class TopoSpaceMiddleware:
    """Vendor-neutral middleware: optimize request context, then call any agent/model executor."""
    def __init__(self,engine,executor):self.engine=engine;self.executor=executor
    def invoke(self,objective,context,agents=None,required_capabilities=None,**kwargs):
        plan=self.engine.optimize(objective,context,agents,required_capabilities)
        result=self.executor(objective=objective,context=plan["context"],team=plan["team"],**kwargs)
        return {"result":result,"optimization":plan}
