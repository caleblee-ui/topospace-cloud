
from __future__ import annotations
from collections import defaultdict
from benchmarking.statistics import mean, bootstrap_ci, paired_reduction, paired_delta

FIELDS=["input_tokens","output_tokens","tool_calls","agent_invocations","latency_ms","cost_usd"]

class ABBenchmarkHarness:
    def __init__(self, adapter, repeats=5):
        self.adapter=adapter; self.repeats=int(repeats)

    def run(self,tasks):
        records=[]
        for task in tasks:
            for i in range(self.repeats):
                records.append(self.adapter.run(task,"baseline",i))
                records.append(self.adapter.run(task,"topospace",i))
        return self.summarize(records)

    def summarize(self,records):
        paired=defaultdict(lambda:{"baseline":{},"topospace":{}})
        for r in records:
            paired[(r.task_id,r.run_index)][r.mode]=r

        summary={"records":[r.to_dict() for r in records],"metrics":{}}
        for field in FIELDS:
            b=[];o=[]
            for key,p in sorted(paired.items()):
                if "baseline" in p and "topospace" in p:
                    b.append(float(getattr(p["baseline"],field)))
                    o.append(float(getattr(p["topospace"],field)))
            reductions=paired_reduction(b,o)
            summary["metrics"][field]={
              "baseline_mean":mean(b),
              "topospace_mean":mean(o),
              "reduction_pct_mean":mean(reductions),
              "reduction_pct_ci95":bootstrap_ci(reductions)
            }

        bsucc=[]; osucc=[]
        for key,p in sorted(paired.items()):
            if "baseline" in p and "topospace" in p:
                bsucc.append(1.0 if p["baseline"].success else 0.0)
                osucc.append(1.0 if p["topospace"].success else 0.0)
        deltas=[100*x for x in paired_delta(bsucc,osucc)]
        summary["success"]={
          "baseline_rate":mean(bsucc),
          "topospace_rate":mean(osucc),
          "delta_pp_mean":mean(deltas),
          "delta_pp_ci95":bootstrap_ci(deltas)
        }
        return summary
