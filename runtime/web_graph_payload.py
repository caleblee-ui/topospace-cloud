
def build_graph_payload(nodes,edges,scores=None,state_id="state"):
    smap={x["id"]:x for x in (scores or [])}
    out_nodes=[]
    for n in nodes:
        nid=n if isinstance(n,str) else n.get("id")
        row=smap.get(nid,{})
        out_nodes.append({
            "id":nid,
            "label":nid if isinstance(n,str) else n.get("label",nid),
            "type":"context" if isinstance(n,str) else n.get("type","context"),
            "score":row.get("score",0.0),
            "components":row.get("components",{}),
            "topological_support":row.get("topological_support",0.0),
        })
    return {"state_id":state_id,"nodes":out_nodes,"edges":[
        {"source":a,"target":b,"distance":float(w),"affinity":max(0.0,1.0-float(w))}
        for a,b,w in edges]}
