
from learned_field.network import CouplingFieldNetwork
from learned_field.models import FieldState
from coupled_geometry.runtime import CrossDomainGeometryRuntime
from coupled_geometry.coupling import CrossDomainCoupling

class LearnedTopologicalFieldRuntime:
    def __init__(self,max_iterations=4):
        self.field=CouplingFieldNetwork()
        self.max_iterations=max_iterations
        self.last_snapshot=None

    def solve(self,agent_state,spaces):
        fs=FieldState(
          risk=agent_state.risk,ambiguity=agent_state.ambiguity,hierarchy=agent_state.hierarchy,
          candidate_pressure=agent_state.candidate_pressure,latency_pressure=agent_state.latency_pressure,
          memory_pressure=float(agent_state.metadata.get("memory_pressure",0)),
          tool_pressure=float(agent_state.metadata.get("tool_pressure",0)),
        )
        snap=self.field.forward(fs);self.last_snapshot=snap
        runtime=CrossDomainGeometryRuntime(max_iterations=self.max_iterations)
        runtime.coupling=CrossDomainCoupling(snap.couplings)
        result=runtime.solve(agent_state,spaces)
        result["field_snapshot"]=snap
        result["field_state"]=fs
        return result

    def feedback(self,solution,rewards):
        snap=self.field.update(solution["field_state"],rewards)
        self.last_snapshot=snap
        return snap
