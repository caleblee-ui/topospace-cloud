
class RuntimeMetrics:
    def __init__(self):self.rows=[]
    def observe(self,task_id,usage,variant,geometry=None):
        self.rows.append({
          "task_id":task_id,"variant":variant,
          "input_tokens":usage.input_tokens,"output_tokens":usage.output_tokens,
          "tool_calls":usage.tool_calls,"latency_ms":usage.latency_ms,
          "success":usage.success,"geometry":geometry or {}
        })
    def summary(self):
        if not self.rows:return {"requests":0}
        return {
          "requests":len(self.rows),
          "success_rate":sum(bool(x["success"]) for x in self.rows)/len(self.rows),
          "mean_input_tokens":sum(x["input_tokens"] for x in self.rows)/len(self.rows),
          "mean_latency_ms":sum(x["latency_ms"] for x in self.rows)/len(self.rows)
        }
