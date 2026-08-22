
from online_learning.service import SafeOnlineJointRuntime
from unified_runtime.models import AgentState
from unified_runtime.cognitive_bridge import RuntimeSpaceBuilder

class JointRuntimeService:
    def __init__(self):
        self.runtime=SafeOnlineJointRuntime()
        self.builder=RuntimeSpaceBuilder()

    def optimize(self,task_id,objective,raw_spaces,state=None):
        state=state or {}
        s=AgentState(task_id,objective,
            risk=float(state.get("risk",0)),
            ambiguity=float(state.get("ambiguity",0)),
            hierarchy=float(state.get("hierarchy",0)),
            candidate_pressure=float(state.get("candidate_pressure",0)),
            latency_pressure=float(state.get("latency_pressure",0)),
            metadata=dict(state.get("metadata",{})))
        spaces={k:self.builder.build_space(v) for k,v in raw_spaces.items()}
        return self.runtime.execute(s,spaces)
