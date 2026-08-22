
from cognitive_topology.layers import CognitiveMemory

class CognitiveTorusBridge:
    """Maps TorusDB memory records to/from cognitive topology records."""
    def import_records(self,layers,records,default_layer="episodic"):
        ids=[]
        for r in records:
            m=CognitiveMemory(
              id=str(r.get("id")),content=str(r.get("content","")),layer=r.get("layer",default_layer),
              importance=float(r.get("importance",.5)),confidence=float(r.get("confidence",r.get("semantic_score",.5))),
              utility=float(r.get("utility",r.get("importance",.5))),distance=float(r.get("distance",1)),
              access_count=int(r.get("access_count",0)),success_count=int(r.get("success_count",0)),
              metadata=dict(r.get("metadata",{}))
            )
            layers.put(m);ids.append(m.id)
        return ids

    def export_record(self,m):
        return {"id":m.id,"content":m.content,"layer":m.layer,"importance":m.importance,
                "confidence":m.confidence,"utility":m.utility,"distance":m.distance,
                "access_count":m.access_count,"success_count":m.success_count,"metadata":m.metadata}
