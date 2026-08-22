
from __future__ import annotations
def team_to_graph_payload(objective, team, step=0):
    nodes=[{"id":"task","label":objective,"type":"state","score":1.0}]
    for a in team.members:
        nodes.append({
            "id":a["id"],"label":a["id"],"type":"agent","score":a.get("score",0.0),
            "components":{
                "reliability":a.get("reliability",1.0),
                "risk":1.0-a.get("risk",0.0),
                "cost_efficiency":1.0-a.get("cost",0.0),
            }
        })
    edges=[{"source":"task","target":a["id"],"distance":max(0,1-a.get("score",0)),"affinity":a.get("score",0),"type":"assignment"} for a in team.members]
    for a,b,w in team.topology_edges:
        edges.append({"source":a,"target":b,"distance":float(w),"affinity":max(0,1-float(w)),"type":"collaboration"})
    return {"state_id":f"team-step-{step}","nodes":nodes,"edges":edges}
