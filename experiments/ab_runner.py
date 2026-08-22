
from dataclasses import asdict
class ABAgentExperiment:
    def __init__(self): self.rows=[]

    def record(self,task_id,baseline_usage,topospace_usage,quality_baseline,quality_topospace):
        b=baseline_usage;t=topospace_usage
        row={
          "task_id":task_id,
          "baseline":asdict(b),"topospace":asdict(t),
          "quality_baseline":float(quality_baseline),
          "quality_topospace":float(quality_topospace),
          "input_token_saving_pct":100*(1-t.input_tokens/max(1,b.input_tokens)),
          "total_token_saving_pct":100*(1-(t.input_tokens+t.output_tokens)/max(1,b.input_tokens+b.output_tokens)),
          "latency_saving_pct":100*(1-t.latency_ms/max(1e-9,b.latency_ms)),
          "tool_call_saving_pct":100*(1-t.tool_calls/max(1,b.tool_calls)),
        }
        self.rows.append(row);return row

    def summary(self):
        if not self.rows:return {"tasks":0}
        mean=lambda k:sum(r[k] for r in self.rows)/len(self.rows)
        return {
          "tasks":len(self.rows),
          "mean_input_token_saving_pct":mean("input_token_saving_pct"),
          "mean_total_token_saving_pct":mean("total_token_saving_pct"),
          "mean_latency_saving_pct":mean("latency_saving_pct"),
          "mean_tool_call_saving_pct":mean("tool_call_saving_pct"),
          "mean_quality_delta":sum(r["quality_topospace"]-r["quality_baseline"] for r in self.rows)/len(self.rows)
        }
