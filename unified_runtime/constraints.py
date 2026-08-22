
class HardConstraintGate:
    """
    Enforces non-compensatory policy/security constraints before geometry ranking.
    For normalized views, a component at or above the configured threshold is excluded.
    """
    def __init__(self,policy_index=3,security_index=4,threshold=1.0):
        self.policy_index=policy_index
        self.security_index=security_index
        self.threshold=float(threshold)

    def filter(self,candidates,enabled=True):
        if not enabled:
            return list(candidates),[]
        kept=[];blocked=[]
        for c in candidates:
            vals=[float(v.value) for v in c["views"]]
            violate=(vals[self.policy_index]>=self.threshold or
                     vals[self.security_index]>=self.threshold)
            (blocked if violate else kept).append(c)
        return kept,blocked
