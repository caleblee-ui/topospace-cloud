
from llm_runtime.topospace_middleware import TopoSpaceMiddleware
from llm_runtime.contracts import LLMRequest

class TopoSpaceAgent:
    def __init__(self,provider,optimizer):
        self.provider=provider
        self.middleware=TopoSpaceMiddleware(optimizer)

    def run(self,task_id,messages,spaces,model="default",state=None,tools=None,metadata=None):
        req=LLMRequest(task_id,messages,model=model,metadata=metadata or {})
        return self.middleware.execute(self.provider,req,spaces,state,tools)
