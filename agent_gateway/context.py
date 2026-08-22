
class ContextBudgeter:
    def __init__(self,min_budget=256):self.min_budget=min_budget
    def budget(self,max_tokens,candidate_pressure=0.0,latency_pressure=0.0):
        pressure=max(0.0,min(1.0,.65*candidate_pressure+.35*latency_pressure))
        return max(self.min_budget,int(max_tokens*(1-.45*pressure)))
