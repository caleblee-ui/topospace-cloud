
class TopoSpaceJointClient:
    """Embedded client for Joint Runtime Service; HTTP transport can wrap the same contract."""
    def __init__(self,service):self.service=service
    def optimize(self,task_id,objective,spaces,state=None):
        return self.service.optimize(task_id,objective,spaces,state)
