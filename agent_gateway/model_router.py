
class ModelRouter:
    """Provider-neutral logical model routing. Physical provider mapping is deployment configuration."""
    def route(self,requested,state):
        if requested and requested!="auto":return requested
        risk=float(state.get("risk",0));ambiguity=float(state.get("ambiguity",0))
        latency=float(state.get("latency_pressure",0))
        if risk>.75 or ambiguity>.8:return "reasoning"
        if latency>.7:return "fast"
        return "balanced"
