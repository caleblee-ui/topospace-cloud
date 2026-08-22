
class FrameworkAdapter:
    """Stable adapter contract for external agent frameworks."""
    name="custom"
    def __init__(self,client):self.client=client
    def task_start(self,*a,**k):return self.client.task_start(*a,**k)
    def memory_recall(self,*a,**k):return self.client.memory_recall(*a,**k)
    def before_model(self,*a,**k):return self.client.before_model(*a,**k)
    def after_model(self,*a,**k):return self.client.after_model(*a,**k)
    def before_tool(self,*a,**k):return self.client.before_tool(*a,**k)
    def after_tool(self,*a,**k):return self.client.after_tool(*a,**k)
    def task_complete(self,*a,**k):return self.client.task_complete(*a,**k)
