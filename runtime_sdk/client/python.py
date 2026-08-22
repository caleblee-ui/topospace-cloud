
from runtime_sdk.http.client import TopoSpaceRuntimeHTTPClient

class TopoSpaceClient:
    def __init__(self,*args,**kwargs):
        self.http=TopoSpaceRuntimeHTTPClient(*args,**kwargs)
    def task_start(self,task_id,**kw):return self.http.dispatch("task_start",task_id,**kw)
    def memory_recall(self,task_id,**kw):return self.http.dispatch("memory_recall",task_id,**kw)
    def before_model(self,task_id,**kw):return self.http.dispatch("before_model",task_id,**kw)
    def after_model(self,task_id,**kw):return self.http.dispatch("after_model",task_id,**kw)
    def before_tool(self,task_id,**kw):return self.http.dispatch("before_tool",task_id,**kw)
    def after_tool(self,task_id,**kw):return self.http.dispatch("after_tool",task_id,**kw)
    def task_complete(self,task_id,**kw):return self.http.dispatch("task_complete",task_id,**kw)
