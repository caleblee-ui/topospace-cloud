
class AutopilotPolicy:
    """Safety envelope for automated parameter changes."""
    def __init__(self,max_token_change=.35,max_epsilon_change=.18,max_p_change=.75):
        self.max_token_change=max_token_change
        self.max_epsilon_change=max_epsilon_change
        self.max_p_change=max_p_change

    @staticmethod
    def _bounded(old,new,max_fraction=None,max_abs=None):
        if old is None:return new
        if max_fraction is not None:
            lo=old*(1-max_fraction);hi=old*(1+max_fraction)
            return max(lo,min(hi,new))
        if max_abs is not None:
            return max(old-max_abs,min(old+max_abs,new))
        return new

    def apply(self,previous,decision):
        if previous is None:return decision
        decision.max_context_tokens=round(self._bounded(previous.max_context_tokens,decision.max_context_tokens,self.max_token_change))
        decision.epsilon=self._bounded(previous.epsilon,decision.epsilon,max_abs=self.max_epsilon_change)
        decision.p=self._bounded(previous.p,decision.p,max_abs=self.max_p_change)
        return decision
