
class ShadowLearner:
    """Runs challenger decisions without applying them to live execution."""
    def __init__(self):
        self.rows=[]
    def observe(self,live_decision,shadow_decision,outcome):
        row={"live":live_decision,"shadow":shadow_decision,"outcome":outcome}
        self.rows.append(row);return row
    def summary(self):
        if not self.rows:return {"count":0}
        better=sum(1 for x in self.rows if x["outcome"].get("shadow_reward",0)>x["outcome"].get("live_reward",0))
        return {"count":len(self.rows),"shadow_better_rate":better/len(self.rows)}
