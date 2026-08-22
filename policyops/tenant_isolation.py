
class TenantLearningIsolation:
    """Prevents cross-tenant policy statistics from mixing by construction."""
    def __init__(self,factory):
        self.factory=factory;self.learners={}

    def get(self,tenant_id,task_type="default"):
        key=(tenant_id,task_type)
        if key not in self.learners:
            self.learners[key]=self.factory()
        return self.learners[key]

    def keys(self): return list(self.learners.keys())
