
from __future__ import annotations
import json,threading
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from torusdb.http_backend import TorusDBHTTPBackend
from torusdb.models import MemoryRecord
from torusdb.bridge import TorusTopoMemoryBridge

class _State:
    data={}

class MockTorusHandler(BaseHTTPRequestHandler):
    def _json(self,status,obj):
        b=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(b)));self.end_headers();self.wfile.write(b)
    def do_POST(self):
        n=int(self.headers.get("content-length","0") or 0);obj=json.loads(self.rfile.read(n) or b"{}")
        if self.path=="/v1/memory/upsert":
            _State.data[obj["id"]]=obj;return self._json(200,{"memory":obj})
        if self.path=="/v1/memory/search":
            q=set(obj.get("query","").lower().split());rows=[]
            for x in _State.data.values():
                text=(x.get("content") or "").lower()
                overlap=len(q & set(text.split()))/max(1,len(q))
                y=dict(x);y["semantic_score"]=max(float(y.get("semantic_score",0)),overlap);y["distance"]=min(float(y.get("distance",1)),1-overlap)
                rows.append(y)
            rows=sorted(rows,key=lambda x:(x.get("distance",1),-x.get("importance",0)))[:obj.get("limit",50)]
            return self._json(200,{"memories":rows})
        return self._json(404,{"error":"not_found"})
    def do_GET(self):
        if self.path.startswith("/v1/memory/"):
            mid=self.path.rsplit("/",1)[-1];x=_State.data.get(mid)
            return self._json(200,{"memory":x}) if x else self._json(404,{"error":"not_found"})
        return self._json(404,{"error":"not_found"})
    def do_DELETE(self):
        if self.path.startswith("/v1/memory/"):
            mid=self.path.rsplit("/",1)[-1];_State.data.pop(mid,None);return self._json(200,{"ok":True})
        return self._json(404,{"error":"not_found"})
    def log_message(self,*args):pass

def run_http_e2e(port=0):
    srv=ThreadingHTTPServer(("127.0.0.1",port),MockTorusHandler)
    actual=srv.server_address[1]
    t=threading.Thread(target=srv.serve_forever,daemon=True);t.start()
    try:
        backend=TorusDBHTTPBackend(f"http://127.0.0.1:{actual}")
        backend.upsert(MemoryRecord("auth","oauth refresh design",importance=.9,distance=.1,tokens=100))
        backend.upsert(MemoryRecord("ui","button spacing",importance=.2,distance=.8,tokens=100))
        result=TorusTopoMemoryBridge(backend).recall("oauth refresh",limit=10,max_return=5)
        return {"ok":bool(result["memories"]) and result["memories"][0]["id"]=="auth","result":result}
    finally:
        srv.shutdown();srv.server_close()
