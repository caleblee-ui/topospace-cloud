
class GatewayTelemetry:
    def __init__(self):self.events=[]
    def emit(self,task_id,decision,usage=None):
        e={"task_id":task_id,"model":decision.model,"token_budget":decision.token_budget,
           "memory":len(decision.selected_memory),"tools":len(decision.selected_tools),
           "skills":len(decision.selected_skills),"plans":len(decision.selected_plans)}
        if usage:
            e.update({"input_tokens":usage.input_tokens,"output_tokens":usage.output_tokens,
                      "tool_calls":usage.tool_calls,"latency_ms":usage.latency_ms,"success":usage.success})
        self.events.append(e);return e
