
from __future__ import annotations
from collections import defaultdict, deque
from topology.simplicial import VietorisRipsComplex

def betti_numbers(nodes, weighted_edges, epsilon):
    """Computes beta_0 and beta_1 for the 1/2-skeleton over Z2.

    beta_0 = connected components
    beta_1 = E - V + C - rank(boundary_2)
    where rank(boundary_2) is computed over GF(2).
    """
    vr=VietorisRipsComplex()
    simplices=vr.build(nodes,weighted_edges,epsilon)
    edges=[s.vertices for s in simplices if len(s.vertices)==2]
    tris=[s.vertices for s in simplices if len(s.vertices)==3]

    adj={n:set() for n in nodes}
    for a,b in edges:
        adj[a].add(b); adj[b].add(a)
    seen=set(); comps=0
    for n in nodes:
        if n in seen: continue
        comps+=1; stack=[n]; seen.add(n)
        while stack:
            u=stack.pop()
            for v in adj[u]:
                if v not in seen:
                    seen.add(v); stack.append(v)

    edge_index={tuple(sorted(e)):i for i,e in enumerate(edges)}
    rows=[]
    for tri in tris:
        a,b,c=tri
        bits=0
        for e in ((a,b),(a,c),(b,c)):
            idx=edge_index.get(tuple(sorted(e)))
            if idx is not None:
                bits ^= (1<<idx)
        rows.append(bits)

    rank=0
    pivots={}
    for r in rows:
        x=r
        while x:
            p=x.bit_length()-1
            if p in pivots: x ^= pivots[p]
            else:
                pivots[p]=x; rank+=1; break

    beta0=comps
    beta1=max(0,len(edges)-len(nodes)+comps-rank)
    return {"beta0":beta0,"beta1":beta1,"vertices":len(nodes),"edges":len(edges),"triangles":len(tris)}
