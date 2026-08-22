
class LayeredTopologicalRecall:
    BONUS={"working":.02,"episodic":.06,"semantic":.10}
    def score(self,m):
        proximity=1-max(0,min(1,m.distance))
        return .31*m.utility+.24*m.confidence+.22*proximity+.13*m.importance+self.BONUS[m.layer]+.10*m.success_rate

    def recall(self,layers,token_budget=2000,limit=12):
        ranked=sorted(layers.all(),key=self.score,reverse=True)
        selected=[];used=0
        for m in ranked:
            tokens=int(m.metadata.get("tokens",100))
            if used+tokens>token_budget and selected:continue
            selected.append(m);used+=tokens
            if len(selected)>=limit:break
        return {"memories":selected,"tokens":used}
