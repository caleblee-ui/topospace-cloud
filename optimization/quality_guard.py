
class QualityPreservationGuard:
    """Controls aggressive pruning using uncertainty/failure feedback."""
    def __init__(self,uncertainty_threshold=.72,min_context_items=2):
        self.uncertainty_threshold=uncertainty_threshold
        self.min_context_items=min_context_items

    def should_expand(self,*,uncertainty,previous_success,kept_items):
        reasons=[]
        if uncertainty>=self.uncertainty_threshold: reasons.append("high_uncertainty")
        if not previous_success: reasons.append("previous_failure")
        if kept_items<self.min_context_items: reasons.append("context_too_small")
        return {"expand":bool(reasons),"reasons":reasons}
