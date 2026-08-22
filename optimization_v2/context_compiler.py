
from __future__ import annotations

class TopologyContextCompiler:
    """Compiles selected topology nodes into a bounded, structured agent context."""
    def compile(self,objective,items,token_budget=4000):
        ordered=sorted(items,key=lambda x:(float(x.get("distance",1)),-float(x.get("score",x.get("utility",0)))))
        blocks=[];used=0
        for x in ordered:
            t=int(x.get("tokens",0))
            if used+t>token_budget and blocks:continue
            blocks.append({
              "id":x.get("id"),"content":x.get("content",""),
              "distance":x.get("distance"),"score":x.get("score",x.get("utility",0)),
              "tokens":t
            });used+=t
        return {
          "objective":objective,
          "topological_context":blocks,
          "context_tokens":used,
          "compiler":"topology-context-v1"
        }
