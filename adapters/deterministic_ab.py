
import random
from benchmarking.adapter import AgentBenchmarkAdapter
from benchmarking.models import RunRecord

class DeterministicABAdapter(AgentBenchmarkAdapter):
    """Offline regression adapter. It simulates measured runs and is NOT external evidence."""
    def run(self,task,mode,run_index):
        seed=hash((task.id,run_index)) & 0xffffffff
        rng=random.Random(seed)
        base={
          "coding":(48000,3600,10,4,14500,.68,.84),
          "tool-use":(36000,2800,14,3,11800,.55,.86),
          "long-horizon":(82000,6400,22,5,26500,1.25,.80),
          "multi-agent":(69000,5100,18,6,22400,1.10,.82),
        }[task.workload]
        inp,out,tools,agents,lat,cost,success_prob=base
        if mode=="topospace":
            factors={
              "coding":(.57,.94,.68,.75,.74,.66,.00),
              "tool-use":(.61,.95,.64,.80,.77,.70,.01),
              "long-horizon":(.49,.92,.59,.72,.69,.61,.01),
              "multi-agent":(.54,.94,.63,.58,.72,.62,.01),
            }[task.workload]
            inp*=factors[0];out*=factors[1];tools*=factors[2];agents*=factors[3];lat*=factors[4];cost*=factors[5];success_prob+=factors[6]
        jitter=lambda x,p=.035: max(0,x*(1+rng.uniform(-p,p)))
        success=rng.random() < success_prob
        return RunRecord(task.id,mode,run_index,success,
          int(jitter(inp)),int(jitter(out)),max(0,round(jitter(tools,.06))),
          max(0,round(jitter(agents,.06))),jitter(lat),jitter(cost),{"workload":task.workload,"synthetic":True})
