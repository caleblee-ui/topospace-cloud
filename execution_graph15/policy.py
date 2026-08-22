
class EscalationPolicy:
    def __init__(self,min_confidence=.65,max_steps=5):
        self.min_confidence=min_confidence;self.max_steps=max_steps

    def should_stop(self,step,signal):
        if step>=self.max_steps:return True
        if signal.get("success") and signal.get("confidence",0)>=self.min_confidence and not signal.get("needs_tool"):
            return True
        return False
