
HOOKS={"task_start","memory_recall","before_model","after_model","before_tool","after_tool","task_complete"}
class HookRegistry:
    def __init__(self):self.handlers={x:[] for x in HOOKS}
    def on(self,hook,handler):
        if hook not in HOOKS:raise ValueError("unknown_hook")
        self.handlers[hook].append(handler);return handler
    def emit(self,event):
        if event.hook not in HOOKS:
            raise ValueError("unknown_hook")
        out=[]
        for fn in self.handlers[event.hook]:out.append(fn(event))
        return out
