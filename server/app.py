
from __future__ import annotations
import json,os,signal,threading
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from production.concurrent_engine import ConcurrentTopoSpaceEngine
from production.auth import APIKeyManager

ENGINE=ConcurrentTopoSpaceEngine()
AUTH=APIKeyManager()
if os.getenv("TOPOSPACE_API_KEY_ID") and os.getenv("TOPOSPACE_API_KEY_SECRET"):
    AUTH.import_key(os.environ["TOPOSPACE_API_KEY_ID"],os.environ["TOPOSPACE_API_KEY_SECRET"])

class Handler(BaseHTTPRequestHandler):
    server_version="TopoSpace/2.1"
    def _json(self,status,obj):
        body=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body)
    def _auth(self):
        if not AUTH._keys:return True
        kid=self.headers.get("x-topospace-key-id","");sec=self.headers.get("x-topospace-key","")
        return AUTH.verify(kid,sec)
    def do_GET(self):
        if self.path=="/health":return self._json(200,{"ok":True,**ENGINE.health()})
        return self._json(404,{"error":"not_found"})
    def do_POST(self):
        if not self._auth():return self._json(401,{"error":"unauthorized"})
        if self.path!="/v1/optimize":return self._json(404,{"error":"not_found"})
        n=int(self.headers.get("content-length","0") or 0);obj=json.loads(self.rfile.read(n) or b"{}")
        try:
            out=ENGINE.optimize(obj.get("objective",""),obj.get("context",[]),obj.get("agents",[]),obj.get("required_capabilities",[]),
                uncertainty=obj.get("uncertainty",.3),drift=obj.get("drift",0),previous_success=obj.get("previous_success",True),
                cost_pressure=obj.get("cost_pressure",.5),complexity=obj.get("complexity",.5))
            self._json(200,out)
        except Exception as e:self._json(500,{"error":str(e)})
    def log_message(self,*args): pass

def run(host="0.0.0.0",port=8787):
    srv=ThreadingHTTPServer((host,port),Handler)
    def stop(*_):ENGINE.shutdown(False);srv.shutdown()
    try:signal.signal(signal.SIGTERM,stop)
    except Exception:pass
    print(f"TopoSpace production server on {host}:{port}")
    srv.serve_forever()
if __name__=="__main__":run(port=int(os.getenv("PORT","8787")))
