
from benchmarking.adapter import AgentBenchmarkAdapter
from benchmarking.models import RunRecord

class RealAgentAdapterTemplate(AgentBenchmarkAdapter):
    """Implement this adapter for a real model/tool environment.

    Requirements:
    - same model/version and temperature for baseline and TopoSpace
    - same task, tool permissions and max turns
    - capture tokenizer-reported input/output tokens from the provider
    - capture actual provider cost or compute from a frozen price manifest
    - record success using an external task evaluator, not the model itself
    """
    def run(self,task,mode,run_index):
        raise NotImplementedError("Connect your real agent/model runner here.")
