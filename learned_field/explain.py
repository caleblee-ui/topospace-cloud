
class FieldExplainer:
    def strongest_edges(self,snapshot,limit=6):
        rows=[]
        for src,dsts in snapshot.couplings.items():
            for dst,w in dsts.items():
                rows.append({"source":src,"target":dst,"weight":w})
        return sorted(rows,key=lambda x:abs(x["weight"]),reverse=True)[:limit]
