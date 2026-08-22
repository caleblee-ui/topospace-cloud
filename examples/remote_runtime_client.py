
from runtime_sdk.client.python import TopoSpaceClient
client=TopoSpaceClient("http://127.0.0.1:8788",tenant_id="acme",agent_id="coding-agent")
client.task_start("task-1",objective="fix authentication issue")
client.before_model("task-1",prompt="inspect auth code")
client.before_tool("task-1",tool_id="repo.search",query="oauth")
client.after_tool("task-1",tool_id="repo.search",success=True,reward=.9)
client.task_complete("task-1",success=True)
print(client.http.snapshot())
