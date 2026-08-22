
from online_learning.models import PolicySnapshot
class MetaPromotionAdapter:
    def snapshots(self,runtime):
        c=runtime.live_metrics;x=runtime.challenger_metrics
        return (
          PolicySnapshot("champion",1,c["reward"],c["success_rate"],c["violation_rate"],c["latency_ms"],c["sample_count"]),
          PolicySnapshot("challenger",2,x["reward"],x["success_rate"],x["violation_rate"],x["latency_ms"],x["sample_count"])
        )
    def check(self,runtime):
        c,x=self.snapshots(runtime)
        return runtime.promotion.evaluate(c,x)
