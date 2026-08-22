
class ExactContainsEvaluator:
    def __init__(self,required=None,forbidden=None):
        self.required=list(required or []);self.forbidden=list(forbidden or [])
    def evaluate(self,text,task=None):
        low=text.lower()
        return all(x.lower() in low for x in self.required) and not any(x.lower() in low for x in self.forbidden)

class CallableEvaluator:
    def __init__(self,fn):self.fn=fn
    def evaluate(self,text,task=None):return bool(self.fn(text,task))
