
from runtime_sdk.middleware import TopoSpaceMiddleware
from runtime_sdk.adapter import AgentRuntimeAdapter

topospace=TopoSpaceMiddleware()
agent=AgentRuntimeAdapter(topospace,"coding-agent")
agent.task_start("task-1",objective="fix authentication bug")
memory=agent.memory_recall("task-1",token_budget=1500)
agent.before_model("task-1",context=memory)
agent.after_model("task-1",decision="inspect repository")
agent.before_tool("task-1","repo.search",query="authentication")
agent.after_tool("task-1","repo.search",True,reward=.9)
agent.task_complete("task-1",True)
print(topospace.snapshot())
