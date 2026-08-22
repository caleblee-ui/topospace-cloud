
from __future__ import annotations
from middleware.hooks import AgentEnvelope,ToolCallEnvelope

class GenericAgentLoop:
    """Reference loop proving TopoSpace is framework-independent."""
    def __init__(self,middleware,model_call,tool_executor=None):
        self.middleware=middleware
        self.model_call=model_call
        self.tool_executor=tool_executor

    def run(self,envelope:AgentEnvelope):
        pre=self.middleware.before_inference(envelope)
        if not pre.allowed:
            return {"success":False,"error":"inference_blocked","metadata":pre.metadata}

        result=self.model_call(pre.payload)

        post=self.middleware.after_inference(envelope,result)
        return {"success":True,"result":post.payload,"metadata":pre.metadata}

    def call_tool(self,envelope:AgentEnvelope,name,args=None,metadata=None):
        call=ToolCallEnvelope(name,args or {},metadata or {})
        pre=self.middleware.before_tool(envelope,call)
        if not pre.allowed:
            return {"success":False,"error":"tool_blocked","metadata":pre.metadata}
        if not self.tool_executor:
            return {"success":False,"error":"no_tool_executor"}
        raw=self.tool_executor(pre.payload)
        post=self.middleware.after_tool(envelope,pre.payload,raw)
        return {"success":True,"result":post.payload}
