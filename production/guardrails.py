
class RuntimeGuardrails:
    def __init__(self,max_agents=4,max_tool_calls=12,max_steps=8):
        self.max_agents=max_agents;self.max_tool_calls=max_tool_calls;self.max_steps=max_steps
    def validate(self,*,agents=0,tool_calls=0,step=0):
        errors=[]
        if agents>self.max_agents:errors.append("agent_budget_exceeded")
        if tool_calls>self.max_tool_calls:errors.append("tool_budget_exceeded")
        if step>=self.max_steps:errors.append("step_budget_exceeded")
        return {"ok":not errors,"errors":errors}
