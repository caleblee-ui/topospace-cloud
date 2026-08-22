
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from autopilot.service import AutopilotTopoSpaceService

SERVICE=AutopilotTopoSpaceService()

class Handler(BaseHTTPRequestHandler):
 def _json(self,status,obj):
  b=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(b)));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  if self.path=="/healthz":return self._json(200,{"ok":True})
  if self.path=="/v1/autopilot/history":return self._json(200,SERVICE.autopilot.recent())
  return self._json(404,{"error":"not_found"})
 def do_POST(self):
  if self.path!="/v1/optimize":return self._json(404,{"error":"not_found"})
  n=int(self.headers.get("content-length","0") or 0);obj=json.loads(self.rfile.read(n) or b"{}")
  return self._json(200,SERVICE.optimize_with_autopilot(obj,self.headers.get("x-topospace-tenant","default"),self.headers.get("x-topospace-project","default")))
 def log_message(self,*args):pass
if __name__=="__main__":ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8787"))),Handler).serve_forever()
