
class PolicyExplainer:
    def explain(self,decision,signals):
        reasons=[]
        if signals.get("uncertainty",0)>.7:reasons.append("High uncertainty widened the topology neighborhood.")
        if signals.get("drift",0)>.45:reasons.append("Topology drift increased context exploration.")
        if signals.get("token_pressure",0)>.65:reasons.append("Token pressure reduced the context budget.")
        if signals.get("memory_hit_rate",1)<.4:reasons.append("Low memory hit rate increased recall depth.")
        if not reasons:reasons.append("Signals were within the stable operating range.")
        return {
          "summary":" ".join(reasons),
          "parameters":{
            "epsilon":decision.get("epsilon"),
            "p":decision.get("p"),
            "max_context_tokens":decision.get("max_context_tokens"),
            "memory_recall_limit":decision.get("memory_recall_limit"),
            "profile":decision.get("profile"),
          }
        }
