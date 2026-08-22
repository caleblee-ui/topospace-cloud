
class AgentRuntimeAdapter:
    """Minimal adapter contract for external agent frameworks."""
    def __init__(self,middleware,agent_id="agent"):
        self.middleware=middleware;self.agent_id=agent_id
    def task_start(self,task_id,**meta):return self.middleware.dispatch("task_start",task_id,self.agent_id,**meta)
    def memory_recall(self,task_id,token_budget=2000):return self.middleware.dispatch("memory_recall",task_id,self.agent_id,token_budget=token_budget)
    def before_model(self,task_id,**payload):return self.middleware.dispatch("before_model",task_id,self.agent_id,**payload)
    def after_model(self,task_id,**payload):return self.middleware.dispatch("after_model",task_id,self.agent_id,**payload)
    def before_tool(self,task_id,tool_id,**payload):return self.middleware.dispatch("before_tool",task_id,self.agent_id,tool_id=tool_id,**payload)
    def after_tool(self,task_id,tool_id,success,reward=None,**payload):
        p={"tool_id":tool_id,"success":success,**payload}
        if reward is not None:p["reward"]=reward
        return self.middleware.dispatch("after_tool",task_id,self.agent_id,**p)
    def task_complete(self,task_id,success=True,**payload):return self.middleware.dispatch("task_complete",task_id,self.agent_id,success=success,**payload)
