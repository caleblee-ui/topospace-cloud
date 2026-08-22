
from __future__ import annotations
import json, os
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server
from runtime.graph_store import GraphStore
from runtime.live_trace import LiveTraceBuffer

STORE=GraphStore(os.environ.get("TOPOSPACE_GRAPH_DB","topospace_graphs.db"))
TRACE=LiveTraceBuffer()

def response(start,status,obj,headers=None):
    body=json.dumps(obj).encode()
    h=[("Content-Type","application/json"),("Content-Length",str(len(body)))]
    if headers:h+=headers
    start(status,h); return [body]

def app(environ,start_response):
    path=environ.get("PATH_INFO","/")
    method=environ.get("REQUEST_METHOD","GET")
    if path=="/health":
        return response(start_response,"200 OK",{"ok":True,"service":"topospace-v1"})
    if path.startswith("/workspaces/") and path.endswith("/graph/latest") and method=="GET":
        wid=path.split("/")[2]
        return response(start_response,"200 OK",STORE.latest(wid) or {"seq":0,"payload":{"nodes":[],"edges":[]}})
    if path.startswith("/workspaces/") and path.endswith("/graph/history") and method=="GET":
        wid=path.split("/")[2]
        qs=parse_qs(environ.get("QUERY_STRING",""))
        limit=int(qs.get("limit",["100"])[0])
        return response(start_response,"200 OK",STORE.history(wid,limit))
    if path.startswith("/workspaces/") and path.endswith("/graph") and method=="POST":
        wid=path.split("/")[2]
        n=int(environ.get("CONTENT_LENGTH","0") or 0)
        obj=json.loads(environ["wsgi.input"].read(n) or b"{}")
        seq=int(obj.get("seq",1))
        payload=obj.get("payload",obj)
        STORE.save(wid,seq,payload)
        TRACE.push("graph.update",wid,payload.get("nodes",[]),payload.get("edges",[]),{"workspace_id":wid})
        return response(start_response,"200 OK",{"ok":True,"seq":seq})
    return response(start_response,"404 Not Found",{"error":"not found"})

if __name__=="__main__":
    port=int(os.environ.get("PORT","8787"))
    print(f"TopoSpace API on :{port}")
    make_server("0.0.0.0",port,app).serve_forever()
