
from benchmarking.harness import ABBenchmarkHarness
class PairedRealRunner:
    def __init__(self,adapter,repeats=5):self.harness=ABBenchmarkHarness(adapter,repeats)
    def run(self,tasks):return self.harness.run(tasks)
