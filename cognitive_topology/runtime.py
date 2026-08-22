
import time
from cognitive_topology.layers import CognitiveTopologyLayers,CognitiveMemory
from cognitive_topology.consolidator import LongTermTopologyConsolidator
from cognitive_topology.recall import LayeredTopologicalRecall
from cognitive_topology.torus_bridge import CognitiveTorusBridge
from self_reorg.closed_loop import SelfReorganizingTopologyRuntime

class TopologicalCognitiveRuntime:
    def __init__(self):
        self.layers=CognitiveTopologyLayers()
        self.consolidator=LongTermTopologyConsolidator()
        self.recall_engine=LayeredTopologicalRecall()
        self.torus=CognitiveTorusBridge()
        self.execution=SelfReorganizingTopologyRuntime()

    def remember(self,id,content,**kwargs):
        return self.layers.put(CognitiveMemory(id=id,content=content,**kwargs))

    def record_use(self,memory_id,success=True,reward=1.0):
        m=self.layers.get(memory_id)
        if not m:return None
        m.access_count+=1;m.success_count+=1 if success else 0;m.last_accessed=time.time()
        m.utility=max(0,min(1,.8*m.utility+.2*(float(reward) if success else 0)))
        return m

    def consolidate(self):
        return self.consolidator.consolidate(self.layers)

    def recall(self,token_budget=2000,limit=12):
        return self.recall_engine.recall(self.layers,token_budget,limit)

    def bind_recall_to_task(self,task_id,token_budget=2000):
        result=self.recall(token_budget)
        records=[self.torus.export_record(m) for m in result["memories"]]
        added=self.execution.ingest_memories(task_id,records)
        return {"added":added,"memories":records,"tokens":result["tokens"]}

    def snapshot(self):
        return {"layers":self.layers.counts(),"memories":[self.torus.export_record(m) for m in self.layers.all()]}
