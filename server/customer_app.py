
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from customer.service import CustomerTopoSpaceService
from admin.service import AdminService
from commercial.errors import TopoSpaceError

SERVICE=CustomerTopoSpaceService()
ADMIN=AdminService(SERVICE.meter)

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,obj):
        body=json.dumps(obj).encode()
        self.send_response(status);self.send_header("content-type","application/json")
        self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body)

    def do_GET(self):
        if self.path=="/healthz":return self._json(200,{"ok":True})
        if self.path.startswith("/admin/usage/"):
            tenant=self.path.split("/")[-1]
            return self._json(200,ADMIN.usage(tenant))
        return self._json(404,{"error":"not_found"})

    def do_POST(self):
        n=int(self.headers.get("content-length","0") or 0)
        obj=json.loads(self.rfile.read(n) or b"{}")
        if self.path=="/v1/optimize":
            tenant=self.headers.get("x-topospace-tenant","default")
            project=self.headers.get("x-topospace-project","default")
            try:return self._json(200,SERVICE.optimize(obj,tenant,project))
            except TopoSpaceError as e:return self._json(e.status,e.to_dict())
        if self.path=="/admin/tenants":
            return self._json(201,ADMIN.create_tenant(obj["tenant_id"],obj.get("plan","standard")))
        return self._json(404,{"error":"not_found"})

    def log_message(self,*args):pass

if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8787"))),Handler).serve_forever()
