
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from runtime_server.service import RuntimeService
from runtime_server.tenant import TenantScope
from runtime_server.auth import APIKeyAuth

SERVICE=RuntimeService()
AUTH=APIKeyAuth()
if os.getenv("TOPOSPACE_API_KEY_ID") and os.getenv("TOPOSPACE_API_KEY_SECRET"):
    AUTH.add(os.environ["TOPOSPACE_API_KEY_ID"],os.environ["TOPOSPACE_API_KEY_SECRET"])

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,obj):
        b=json.dumps(obj).encode()
        self.send_response(status)
        self.send_header("content-type","application/json")
        self.send_header("content-length",str(len(b)))
        self.end_headers();self.wfile.write(b)
    def _authorized(self):
        if not AUTH.keys:return True
        return AUTH.verify(self.headers.get("x-topospace-key-id",""),self.headers.get("x-topospace-key",""))
    def _scope(self):
        return TenantScope(
          self.headers.get("x-topospace-tenant","default"),
          self.headers.get("x-topospace-project","default"),
          self.headers.get("x-topospace-agent","agent")
        )
    def do_GET(self):
        if self.path=="/healthz":return self._json(200,{"ok":True})
        if self.path=="/readyz":return self._json(200,{"ok":True,"tenants":len(SERVICE.tenants)})
        if self.path=="/v1/runtime/snapshot":
            s=self._scope();return self._json(200,SERVICE.snapshot(s.tenant_id))
        return self._json(404,{"error":"not_found"})
    def do_POST(self):
        if not self._authorized():return self._json(401,{"error":"unauthorized"})
        if not self.path.startswith("/v1/runtime/"):
            return self._json(404,{"error":"not_found"})
        hook=self.path.rsplit("/",1)[-1]
        n=int(self.headers.get("content-length","0") or 0)
        obj=json.loads(self.rfile.read(n) or b"{}")
        task_id=obj.pop("task_id",None)
        if not task_id:return self._json(400,{"error":"task_id_required"})
        try:
            out=SERVICE.dispatch(self._scope(),hook,task_id,obj)
            return self._json(200,{"ok":True,"hook":hook,"result":out})
        except (AttributeError,ValueError) as e:
            return self._json(400,{"error":str(e)})
    def log_message(self,*args):pass

if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8788"))),Handler).serve_forever()
