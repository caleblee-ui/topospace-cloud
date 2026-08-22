
from runtime_sdk.events import RuntimeEvent
from runtime_sdk.hooks import HookRegistry
from cognitive_topology.runtime import TopologicalCognitiveRuntime
from collective_topology.runtime import CollectiveTopologyRuntime
from consensus_topology.runtime import TopologicalMultiAgentConsensusRuntime

class TopoSpaceMiddleware:
    """Framework-agnostic lifecycle middleware for agent runtimes."""
    def __init__(self):
        self.hooks=HookRegistry()
        self.cognitive=TopologicalCognitiveRuntime()
        self.collective=CollectiveTopologyRuntime()
        self.consensus=TopologicalMultiAgentConsensusRuntime()
        self.tasks={}
        self._install_defaults()

    def _install_defaults(self):
        self.hooks.on("task_start",self._task_start)
        self.hooks.on("memory_recall",self._memory_recall)
        self.hooks.on("after_tool",self._after_tool)
        self.hooks.on("task_complete",self._task_complete)

    def dispatch(self,hook,task_id,agent_id=None,**payload):
        ev=RuntimeEvent(hook,task_id,agent_id,payload)
        return self.hooks.emit(ev)

    def _task_start(self,e):
        self.tasks[e.task_id]={"agent_id":e.agent_id,"started_at":e.ts,"events":0}
        if e.task_id not in self.cognitive.execution.graph.nodes:
            self.cognitive.execution.add(e.task_id,"task",score=1,distance=0)
        return {"task_id":e.task_id,"status":"started"}

    def _memory_recall(self,e):
        budget=int(e.payload.get("token_budget",2000))
        return self.cognitive.bind_recall_to_task(e.task_id,budget)

    def _after_tool(self,e):
        tid=e.payload.get("tool_id");success=bool(e.payload.get("success",False));reward=float(e.payload.get("reward",1 if success else 0))
        if tid and self.cognitive.layers.get(tid):self.cognitive.record_use(tid,success,reward)
        return {"tool_id":tid,"success":success,"reward":reward}

    def _task_complete(self,e):
        moved=self.cognitive.consolidate()
        state=self.tasks.setdefault(e.task_id,{})
        state["completed_at"]=e.ts;state["success"]=bool(e.payload.get("success",True))
        return {"consolidated":moved,"success":state["success"]}

    def snapshot(self):
        return {"tasks":self.tasks,"cognitive":self.cognitive.snapshot(),"collective":self.collective.snapshot()}
