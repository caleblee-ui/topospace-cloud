
class GeometryCouplingAdapter:
    """Transforms source-domain selections into target-domain geometry pressure."""
    def selection_strength(self,route):
        selected=route.get("selected",[])
        if not selected:
            return 0.0
        # closer selected candidates imply stronger confidence in the local neighborhood
        ds=[float(x["geometry"]["distance"]) for x in selected if "geometry" in x]
        if not ds:
            return min(1.0,len(selected)/8)
        return max(0.0,min(1.0,1-sum(ds)/len(ds)))

    def adapt_state(self,base_state,domain,total_influence):
        s=dict(
          risk=base_state.risk,
          ambiguity=base_state.ambiguity,
          hierarchy=base_state.hierarchy,
          candidate_pressure=base_state.candidate_pressure,
          latency_pressure=base_state.latency_pressure,
        )
        # Cross-domain evidence lowers ambiguity but increases hierarchy/planning structure.
        s["ambiguity"]=max(0.0,min(1.0,s["ambiguity"]-.25*total_influence))
        if domain=="plan":
            s["hierarchy"]=max(0.0,min(1.0,s["hierarchy"]+.35*total_influence))
        if domain=="tool":
            s["risk"]=max(0.0,min(1.0,s["risk"]+.12*max(0,total_influence)))
        if domain=="memory":
            s["candidate_pressure"]=max(0.0,min(1.0,s["candidate_pressure"]-.15*total_influence))
        return s
