
class MetaRuntimeObservability:
    def __init__(self):self.rows=[]
    def emit(self,task_id,decision,usage=None,variant="champion"):
        meta=decision["meta"]
        row={"task_id":task_id,"variant":variant,"geometry":meta.geometry_family,
             "model":meta.model,"path":meta.path,"score":meta.score}
        if usage:
            row.update({"input_tokens":usage.input_tokens,"output_tokens":usage.output_tokens,
                        "tool_calls":usage.tool_calls,"latency_ms":usage.latency_ms,"success":usage.success})
        self.rows.append(row);return row
    def summary(self):
        if not self.rows:return {"requests":0}
        return {"requests":len(self.rows),
                "mean_meta_score":sum(x["score"] for x in self.rows)/len(self.rows)}
