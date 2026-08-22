
class MetaPolicyGuardrail:
    """
    Applies deterministic overrides after the learned meta-policy.
    """
    def apply(self,agent_state,decision):
        overrides=[]
        meta=decision["meta"]
        if agent_state.risk>=.9 and meta.model=="fast":
            meta.model="reasoning";overrides.append("high_risk_model")
        if agent_state.risk>=.9 and "reasoning" not in meta.path:
            candidates=decision["graph_route"]["ranking"]
            for row in candidates:
                if "reasoning" in row["stages"]:
                    meta.path=row["path"];overrides.append("high_risk_path");break
        if agent_state.risk>=.8 and meta.geometry_family=="lp":
            # Keep geometry decision explainable; hard constraints still remain outside it.
            overrides.append("review_compensatory_geometry")
        decision["meta_overrides"]=overrides
        return decision
