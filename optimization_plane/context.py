
class ContextCompactor:
 """Selects topology-relevant context under a token budget."""
 def compact(self,items,max_tokens):
  ranked=sorted(items,key=lambda x:(x.get("relevance",0)*x.get("utility",1))/(1+max(0,x.get("distance",0))),reverse=True)
  out=[];used=0
  for x in ranked:
   c=int(x.get("tokens",0))
   if used+c<=max_tokens:out.append(x);used+=c
  return {"items":out,"tokens":used}
