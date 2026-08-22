
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from commercial.service import CommercialTopoSpaceService
from commercial.errors import TopoSpaceError
from commercial.health import HealthRegistry
from production.auth import APIKeyManager
SERVICE=CommercialTopoSpaceService();AUTH=APIKeyManager();HEALTH=HealthRegistry()
HEALTH.register("engine",lambda:{"ok":True,"version":SERVICE.VERSION});HEALTH.register("sla",lambda:{"ok":True,**SERVICE.sla.snapshot()})
if os.getenv("TOPOSPACE_API_KEY_ID") and os.getenv("TOPOSPACE_API_KEY_SECRET"): AUTH.import_key(os.environ["TOPOSPACE_API_KEY_ID"],os.environ["TOPOSPACE_API_KEY_SECRET"])
class Handler(BaseHTTPRequestHandler):
    server_version="TopoSpace/3.0"
    def _json(self,status,obj,headers=None):
        body=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(body)));self.send_header("x-topospace-version",SERVICE.VERSION)
        if headers:
            for k,v in headers.items():self.send_header(k,str(v))
        self.end_headers();self.wfile.write(body)
    def _authorized(self):
        if not AUTH._keys:return True
        return AUTH.verify(self.headers.get("x-topospace-key-id",""),self.headers.get("x-topospace-key",""))
    def do_GET(self):
        if self.path=="/healthz":return self._json(200,{"ok":True})
        if self.path=="/readyz":
            h=HEALTH.snapshot();return self._json(200 if h["ok"] else 503,h)
        if self.path=="/v1/sla":return self._json(200,SERVICE.sla.snapshot())
        return self._json(404,{"error":{"code":"NOT_FOUND","message":"not found","retryable":False}})
    def do_POST(self):
        if self.path!="/v1/optimize":return self._json(404,{"error":{"code":"NOT_FOUND","message":"not found","retryable":False}})
        if not self._authorized():return self._json(401,{"error":{"code":"UNAUTHORIZED","message":"invalid API key","retryable":False}})
        n=int(self.headers.get("content-length","0") or 0)
        try:obj=json.loads(self.rfile.read(n) or b"{}")
        except Exception:return self._json(400,{"error":{"code":"INVALID_JSON","message":"invalid json","retryable":False}})
        try:
            out=SERVICE.optimize(obj,self.headers.get("x-topospace-tenant","default"),self.headers.get("x-topospace-project","default"));return self._json(200,out,{"x-request-id":out["request_id"]})
        except TopoSpaceError as e:return self._json(e.status,e.to_dict())
    def log_message(self,*args):pass
if __name__=="__main__":ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8787"))),Handler).serve_forever()
