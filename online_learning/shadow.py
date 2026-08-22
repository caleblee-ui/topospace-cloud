
class ShadowJointEvaluator:
    def __init__(self):self.rows=[]
    def observe(self,champion_score,challenger_score,violations=0):
        self.rows.append({
          "champion":float(champion_score),
          "challenger":float(challenger_score),
          "violations":int(violations)
        })
    def summary(self):
        if not self.rows:return {"samples":0,"challenger_win_rate":0.0,"mean_gain":0.0,"violations":0}
        wins=sum(1 for r in self.rows if r["challenger"]>r["champion"])
        gains=[r["challenger"]-r["champion"] for r in self.rows]
        return {
          "samples":len(self.rows),
          "challenger_win_rate":wins/len(self.rows),
          "mean_gain":sum(gains)/len(gains),
          "violations":sum(r["violations"] for r in self.rows)
        }
