
import time

class LongTermTopologyConsolidator:
    """Promotes useful working memories to episodic/semantic topology."""
    def __init__(self,episodic_threshold=.62,semantic_threshold=.78):
        self.episodic_threshold=episodic_threshold
        self.semantic_threshold=semantic_threshold

    def strength(self,m):
        recency=1/(1+max(0,time.time()-m.last_accessed)/86400)
        repetition=min(1,m.access_count/8)
        return .28*m.importance+.22*m.confidence+.24*m.utility+.16*m.success_rate+.06*repetition+.04*recency

    def target_layer(self,m):
        s=self.strength(m)
        if m.access_count>=4 and m.success_rate>=.7 and s>=self.semantic_threshold:return "semantic"
        if m.access_count>=2 and s>=self.episodic_threshold:return "episodic"
        return "working"

    def consolidate(self,layers):
        moved=[]
        for m in list(layers.all()):
            target=self.target_layer(m)
            if target!=m.layer:
                before=m.layer;m.layer=target;layers.put(m);moved.append({"id":m.id,"from":before,"to":target,"strength":self.strength(m)})
        return moved
