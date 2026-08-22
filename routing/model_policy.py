
class ModelRoutingPolicy:
    def choose_tier(self,complexity,uncertainty,cost_pressure):
        need=.55*complexity+.45*uncertainty-.25*cost_pressure
        if need<.30:return "small"
        if need<.65:return "medium"
        return "large"
