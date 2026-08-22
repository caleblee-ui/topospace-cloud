from __future__ import annotations
from dataclasses import dataclass,asdict
from time import perf_counter
from coding.repository import RepositoryIngestor
from coding.context import CodingContextIndex
from coding.tools import CodingTools
from coding.model import ReferenceCodingModel

@dataclass
class RunMetrics:
    success: bool; steps:int; files_read:int; tool_calls:int; context_objects:int; context_chars:int; latency_ms:float

class CodingAgent:
    def __init__(self, root, selector, model=None, event_bus=None, workspace_id='default'):
        self.root=root; self.selector=selector; self.model=model or ReferenceCodingModel(); self.events=event_bus; self.workspace_id=workspace_id
    def _emit(self,event,payload):
        if self.events:self.events.publish(event,self.workspace_id,payload)
    def run(self,task,max_steps=6):
        t0=perf_counter(); records=RepositoryIngestor().ingest(self.root); idx=CodingContextIndex.build(records)
        context=self.selector(idx,task); tools=CodingTools(self.root); obs=[]; success=False
        self._emit('context.selected',{'task':task,'nodes':[getattr(o,'metadata',{}).get('path') for o in context]})
        for step in range(max_steps):
            d=self.model.decide(task=task,context=context,observations=obs); self._emit('agent.action',{'step':step,'action':d.action,'path':d.path,'reason':d.reason})
            if d.action=='read' and d.path: obs.append({'kind':'read','path':d.path,'content':tools.read(d.path)[:4000]})
            elif d.action=='patch' and d.path:
                ok=tools.patch_reference(d.path,task); obs.append({'kind':'patched','path':d.path,'ok':ok})
            elif d.action=='test':
                code,out=tools.test(); obs.append({'kind':'test','code':code,'output':out[-4000:]}); success=(code==0); self._emit('test.result',{'success':success,'code':code}); break
            else: break
        chars=sum(len(getattr(idx.records.get(getattr(o,'metadata',{}).get('path','')),'content','')) for o in context)
        return RunMetrics(success,len(obs),tools.read_count,tools.tool_calls,len(context),chars,(perf_counter()-t0)*1000),obs

def semantic_selector(k=8):
    def select(idx,task):
        from index.ann import ANNIndex
        ann=ANNIndex(128);ann.build(idx.embeddings.items()); q=idx.provider.embed(task); ids=[x[0] for x in ann.query(q,k)]
        by={o.metadata['path']:o for o in idx.objects(task)}
        return [by[p] for p in ids if p in by]
    return select

def topological_selector(k=8):
    def select(idx,task):
        import math
        q=idx.provider.embed(task); objs=idx.objects(task); ranked=[]
        for o in objs:
            sem=1-sum(x*y for x,y in zip(q,o.features['semantic']))
            structural=o.features['structural']; risk=o.features['risk']; cost=o.features['cost']
            # task-conditioned composite Lp reference for coding context
            p=1.5 if any(t in task.lower() for t in ['auth','security','token']) else 2.0
            w={'semantic':0.45,'structural':3.0,'risk':0.35,'cost':0.15}
            d=(w['semantic']*max(0,sem)**p+w['structural']*structural**p+w['risk']*risk**p+w['cost']*cost**p)**(1/p)
            ranked.append((d,o))
        ranked.sort(key=lambda x:x[0]); return [o for _,o in ranked[:k]]
    return select
