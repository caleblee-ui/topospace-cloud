
class OfflineReplay:
    """Re-evaluates a policy over recorded observation rows without sending live traffic."""
    def run(self,policy_fn,rows):
        results=[]
        for row in rows:
            decision=policy_fn(row["signals"])
            score=row["evaluator"](decision,row)
            results.append(score)
        if not results:return {"count":0,"mean_reward":0,"success_rate":0}
        return {
          "count":len(results),
          "mean_reward":sum(x.get("reward",0) for x in results)/len(results),
          "success_rate":sum(1 for x in results if x.get("success"))/len(results),
          "mean_cost":sum(x.get("cost",0) for x in results)/len(results),
        }
