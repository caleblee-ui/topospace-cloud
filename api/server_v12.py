
from __future__ import annotations
import json, os, time
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server, WSGIRequestHandler
from runtime.graph_store import GraphStore
from runtime.event_broker import EventBroker

STORE=GraphStore(os.environ.get("TOPOSPACE_GRAPH_DB","topospace_graphs.db"))
BROKER=EventBroker()

def jresponse(start,status,obj):
    body=json.dumps(obj).encode()
    start(status,[("Content-Type","application/json"),("Content-Length",str(len(body))),("Access-Control-Allow-Origin","*")])
    return [body]

def read_json(env):
    n=int(env.get("CONTENT_LENGTH","0") or 0)
    return json.loads(env["wsgi.input"].read(n) or b"{}")

def sse(start, workspace_id, since):
    rows=BROKER.wait_since(workspace_id,since,timeout=1.0)
    chunks=[]
    if not rows:
        chunks.append(": keepalive\\n\\n")
    else:
        for row in rows:
            chunks.append("event: topology\\ndata: "+json.dumps(row)+"\\n\\n")
    body="".join(chunks).encode()
    start("200 OK",[
      ("Content-Type","text/event-stream"),
      ("Cache-Control","no-cache"),
      ("Access-Control-Allow-Origin","*"),
      ("Content-Length",str(len(body)))
    ])
    return [body]

def app(env,start):
    path=env.get("PATH_INFO","/"); method=env.get("REQUEST_METHOD","GET")
    if method=="OPTIONS":
        start("204 No Content",[("Access-Control-Allow-Origin","*"),("Access-Control-Allow-Methods","GET,POST,OPTIONS"),("Access-Control-Allow-Headers","Content-Type")]);return [b""]
    if path=="/health":return jresponse(start,"200 OK",{"ok":True,"service":"topospace-v1.2"})
    parts=[p for p in path.split("/") if p]
    if len(parts)>=3 and parts[0]=="workspaces":
        wid=parts[1]
        if parts[2]=="events" and method=="GET":
            qs=parse_qs(env.get("QUERY_STRING","")); since=int(qs.get("since",["0"])[0]);return sse(start,wid,since)
        if parts[2]=="graph":
            if len(parts)==4 and parts[3]=="latest" and method=="GET":
                return jresponse(start,"200 OK",STORE.latest(wid) or {"seq":0,"payload":{"nodes":[],"edges":[]}})
            if len(parts)==4 and parts[3]=="history" and method=="GET":
                qs=parse_qs(env.get("QUERY_STRING",""));return jresponse(start,"200 OK",STORE.history(wid,int(qs.get("limit",["100"])[0])))
            if len(parts)==3 and method=="POST":
                obj=read_json(env); seq=int(obj.get("seq",1)); payload=obj.get("payload",obj)
                STORE.save(wid,seq,payload)
                frame={"seq":seq,"workspace_id":wid,"event":"graph.update","payload":payload,"ts":time.time()}
                BROKER.publish(wid,frame)
                return jresponse(start,"200 OK",{"ok":True,"seq":seq})
    return jresponse(start,"404 Not Found",{"error":"not found"})

if __name__=="__main__":
    port=int(os.environ.get("PORT","8787"));print(f"TopoSpace v1.2 API on :{port}")
    make_server("0.0.0.0",port,app,handler_class=WSGIRequestHandler).serve_forever()
