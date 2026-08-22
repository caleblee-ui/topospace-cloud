
def instrument_tool(adapter,task_id,tool_id):
    def deco(fn):
        def wrapped(*args,**kwargs):
            adapter.before_tool(task_id,tool_id,args=args,kwargs=kwargs)
            try:
                result=fn(*args,**kwargs)
                adapter.after_tool(task_id,tool_id,True,reward=1)
                return result
            except Exception:
                adapter.after_tool(task_id,tool_id,False,reward=0)
                raise
        return wrapped
    return deco
