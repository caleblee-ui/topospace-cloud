
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from production.concurrent_engine import ConcurrentTopoSpaceEngine
from enterprise.rbac import RBAC,Principal
from enterprise.policy import PolicyEngine
from enterprise.audit import AuditLog
from enterprise.metrics import MetricsRegistry

ENGINE=ConcurrentTopoSpaceEngine()
RBAC_ENGINE=RBAC();POLICIES=PolicyEngine()
AUDIT=AuditLog(os.getenv("TOPOSPACE_AUDIT_DB","topospace_audit.db"))
METRICS=MetricsRegistry()

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,obj):
        body=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body)
    def principal(self):
        roles=set(filter(None,self.headers.get("x-topospace-roles","developer").split(",")))
        projects=set(filter(None,self.headers.get("x-topospace-projects","").split(",")))
        return Principal(self.headers.get("x-topospace-principal","anonymous"),roles,self.headers.get("x-topospace-org","default"),projects)
    def do_GET(self):
        if self.path=="/health":return self._json(200,{"ok":True,**ENGINE.health()})
        if self.path=="/metrics":
            body=METRICS.prometheus().encode();self.send_response(200);self.send_header("content-type","text/plain; version=0.0.4");self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body);return
        return self._json(404,{"error":"not_found"})
    def do_POST(self):
        if self.path!="/v1/optimize":return self._json(404,{"error":"not_found"})
        p=self.principal();project=self.headers.get("x-topospace-project")
        if not RBAC_ENGINE.authorize(p,"optimize",project):return self._json(403,{"error":"forbidden"})
        n=int(self.headers.get("content-length","0") or 0);obj=json.loads(self.rfile.read(n) or b"{}")
        METRICS.inc("topospace_requests_total",labels={"org":p.org_id})
        out=ENGINE.optimize(obj.get("objective",""),obj.get("context",[]),obj.get("agents",[]),obj.get("required_capabilities",[]),
          uncertainty=obj.get("uncertainty",.3),drift=obj.get("drift",0),previous_success=obj.get("previous_success",True),
          cost_pressure=obj.get("cost_pressure",.5),complexity=obj.get("complexity",.5))
        policy=POLICIES.effective(p.org_id,project)
        check=POLICIES.validate_context(policy,out.get("context",[]),out.get("team",[]))
        AUDIT.append(p.id,"optimize",project or "default",{"objective":obj.get("objective",""),"policy_ok":check["ok"]})
        if not check["ok"]:return self._json(403,{"error":"policy_violation","details":check})
        return self._json(200,out)
    def log_message(self,*args):pass

if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8787"))),Handler).serve_forever()
