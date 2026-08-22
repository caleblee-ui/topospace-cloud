
class JointReplayEvaluator:
    """Offline replay for candidate joint-geometry policies."""
    def evaluate(self,policy_fn,rows):
        rewards=[];success=0;violations=0;lat=[]
        for row in rows:
            out=policy_fn(row["state"],row["spaces"])
            score=float(row["evaluator"](out,row))
            rewards.append(score)
            success+=1 if score>0 else 0
            violations+=int(row.get("violations",0))
            lat.append(float(row.get("latency_ms",0)))
        n=max(1,len(rows))
        return {
          "samples":len(rows),
          "mean_reward":sum(rewards)/n if rewards else 0.0,
          "success_rate":success/n if rows else 0.0,
          "violation_rate":violations/n if rows else 0.0,
          "mean_latency_ms":sum(lat)/n if lat else 0.0,
        }
