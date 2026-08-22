
from abc import ABC, abstractmethod
from benchmarking.models import BenchmarkTask, RunRecord

class AgentBenchmarkAdapter(ABC):
    @abstractmethod
    def run(self, task: BenchmarkTask, mode: str, run_index: int) -> RunRecord:
        """mode is typically 'baseline' or 'topospace'."""
        raise NotImplementedError
