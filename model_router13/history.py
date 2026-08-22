
from collections import defaultdict
class ModelOutcomeHistory:
    def __init__(self):
        self.rows=defaultdict(lambda:{"n":0,"reward":0.0,"success":0,"latency":0.0})

    def record(self,model,reward,success,latency_ms):
        r=self.rows[model]
        r["n"]+=1;r["reward"]+=float(reward);r["success"]+=1 if success else 0;r["latency"]+=float(latency_ms)

    def stats(self,model):
        r=self.rows[model]
        if not r["n"]:
            return {"n":0,"mean_reward":.5,"success_rate":.5,"mean_latency_ms":0.0}
        return {
          "n":r["n"],
          "mean_reward":r["reward"]/r["n"],
          "success_rate":r["success"]/r["n"],
          "mean_latency_ms":r["latency"]/r["n"]
        }
