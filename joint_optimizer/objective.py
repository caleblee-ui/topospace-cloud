
class JointUtility:
    """Unified objective for local geometry and cross-domain field."""
    def __init__(self,w_reward=1.0,w_token=.2,w_latency=.15,w_violation=2.0,w_instability=.25):
        self.w_reward=w_reward
        self.w_token=w_token
        self.w_latency=w_latency
        self.w_violation=w_violation
        self.w_instability=w_instability

    def score(self,obj):
        return (
          self.w_reward*obj.task_reward
          - self.w_token*obj.token_cost
          - self.w_latency*obj.latency_cost
          - self.w_violation*obj.violations
          - self.w_instability*obj.instability
        )
