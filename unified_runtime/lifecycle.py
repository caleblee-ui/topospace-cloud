
class UnifiedRuntimeLifecycle:
    def __init__(self,unified_runtime,space_builder):
        self.runtime=unified_runtime
        self.builder=space_builder

    def prepare(self,agent_state,raw_spaces):
        spaces={k:self.builder.build_space(v) for k,v in raw_spaces.items()}
        return self.runtime.build_execution_space(agent_state,spaces)

    def complete(self,execution_result,feedback):
        return self.runtime.learn(execution_result,feedback)
