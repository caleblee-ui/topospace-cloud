
def normalize(items,kind):
    out=[]
    for i,x in enumerate(items):
        x=dict(x)
        x.setdefault("id",f"{kind}-{i}")
        x.setdefault("kind",kind)
        x.setdefault("semantic_distance",.5)
        x.setdefault("structural_distance",.5)
        x.setdefault("history_distance",.5)
        x.setdefault("policy_distance",0)
        x.setdefault("security_distance",0)
        x.setdefault("cost_distance",.3)
        x.setdefault("reliability_distance",.3)
        out.append(x)
    return out

def request_spaces(req):
    return {
      "memory":normalize(req.memory,"memory"),
      "tool":normalize(req.tools,"tool"),
      "skill":normalize(req.skills,"skill"),
      "plan":normalize(req.plans,"plan")
    }
