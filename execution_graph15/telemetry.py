
class ExecutionGraphTelemetry:
    def __init__(self):self.rows=[]
    def record(self,task_id,path,total_tokens,total_latency_ms,total_cost,success):
        row={"task_id":task_id,"path":list(path),"steps":len(path),"tokens":int(total_tokens),
             "latency_ms":float(total_latency_ms),"cost":float(total_cost),"success":bool(success)}
        self.rows.append(row);return row
    def summary(self):
        if not self.rows:return {"tasks":0}
        return {
          "tasks":len(self.rows),
          "mean_steps":sum(x["steps"] for x in self.rows)/len(self.rows),
          "success_rate":sum(x["success"] for x in self.rows)/len(self.rows),
          "mean_tokens":sum(x["tokens"] for x in self.rows)/len(self.rows),
          "mean_cost":sum(x["cost"] for x in self.rows)/len(self.rows)
        }
