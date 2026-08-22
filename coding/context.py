from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List
from core.objects import TopoObject
from index.embeddings import HashEmbeddingProvider
from coding.repository import CodeRecord, CodeGraph
import math, time

def cosine_distance(a,b):
    dot=sum(x*y for x,y in zip(a,b));na=math.sqrt(sum(x*x for x in a));nb=math.sqrt(sum(y*y for y in b))
    return 1.0-(dot/(na*nb) if na and nb else 0.0)

@dataclass
class CodingContextIndex:
    records: Dict[str,CodeRecord]
    graph: CodeGraph
    embeddings: Dict[str,List[float]]
    provider: HashEmbeddingProvider

    @classmethod
    def build(cls, records):
        provider=HashEmbeddingProvider(128); graph=CodeGraph(records)
        embeddings={r.path:provider.embed(r.path+' '+' '.join(r.symbols)+' '+r.content[:12000]) for r in records}
        return cls({r.path:r for r in records},graph,embeddings,provider)

    def state(self, task: str) -> TopoObject:
        return TopoObject('task:current','STATE',{
            'semantic':self.provider.embed(task),'structural':0.0,'temporal':0.0,'risk':0.0,'cost':0.0,'reliability':1.0
        },{'task':task})

    def objects(self, task: str):
        q=self.provider.embed(task); now=time.time(); out=[]
        terms=set(task.lower().replace('/',' ').replace('_',' ').split())
        if 'authentication' in terms: terms.add('auth')
        if 'comparison' in terms: terms.add('compare')
        if 'vulnerability' in terms: terms.add('security')
        for path,r in self.records.items():
            text=(path+' '+' '.join(r.symbols)+' '+r.content).lower()
            lexical=min(1.0,sum(1 for t in terms if t and t in text)/max(1,len(terms)))
            path_tokens=set(path.lower().replace('/',' ').replace('_',' ').replace('.',' ').split())
            symbol_text=' '.join(r.symbols).lower().replace('_',' ')
            path_match=sum(1 for t in terms if t in path_tokens) / max(1,len(terms))
            symbol_match=sum(1 for t in terms if t and t in symbol_text) / max(1,len(terms))
            operational=min(1.0, 0.35*lexical + 0.35*path_match + 0.30*symbol_match)
            out.append(TopoObject('code:'+path,'CODE',{
                'semantic':self.embeddings[path],
                'structural':1.0-operational,
                'temporal':0.0,'risk':0.25 if any(x in text for x in ['auth','security','token']) else 0.0,
                'cost':min(1.0,len(r.content)/20000.0),'reliability':1.0
            },{'path':path,'symbols':r.symbols,'digest':r.digest}))
        return out
