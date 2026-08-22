
class GeometryStabilityMonitor:
    def distance(self,prev,current):
        if prev is None:return 0.0
        eps=abs(prev["geometry"].epsilon-current["geometry"].epsilon)
        p=abs(prev["geometry"].p-current["geometry"].p)/3.0
        family=0 if prev["geometry"].aggregator==current["geometry"].aggregator else 1.0
        # Mean coupling change.
        diffs=[]
        for src,row in prev["field"].couplings.items():
            for dst,w in row.items():
                diffs.append(abs(w-current["field"].couplings[src][dst]))
        field=sum(diffs)/max(1,len(diffs))
        return .3*eps+.2*p+.25*family+.25*field
