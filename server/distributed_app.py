
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from production.concurrent_engine import ConcurrentTopoSpaceEngine
from production.quota import QuotaManager
from production.circuit_breaker import CircuitBreaker
from production.idempotency import IdempotencyStore
from production.trace import RequestTrace

ENGINE=ConcurrentTopoSpaceEngine()
QUOTA=QuotaManager()
BREAKER=CircuitBreaker()
IDEMP=IdempotencyStore()

class Handler(BaseHTTPRequestHandler):
    def _json(self,status,obj):
        body=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=="/health":return self._json(200,{"ok":True,"circuit_open":not BREAKER.allow(),**ENGINE.health()})
        return self._json(404,{"error":"not_found"})
    def do_POST(self):
        if self.path!="/v1/optimize":return self._json(404,{"error":"not_found"})
        tenant=self.headers.get("x-topospace-tenant","default");idem=self.headers.get("idempotency-key")
        if idem:
            hit=IDEMP.get(tenant+":"+idem)
            if hit is not None:return self._json(200,hit)
        if not BREAKER.allow():return self._json(503,{"error":"circuit_open"})
        admitted=QUOTA.admit(tenant)
        if not admitted["ok"]:return self._json(429,{"error":admitted["reason"]})
        tr=RequestTrace(self.headers.get("x-trace-id"));tr.add("admitted",tenant=tenant)
        try:
            n=int(self.headers.get("content-length","0") or 0);obj=json.loads(self.rfile.read(n) or b"{}")
            tr.add("optimize.start")
            out=ENGINE.optimize(obj.get("objective",""),obj.get("context",[]),obj.get("agents",[]),obj.get("required_capabilities",[]),
              uncertainty=obj.get("uncertainty",.3),drift=obj.get("drift",0),previous_success=obj.get("previous_success",True),
              cost_pressure=obj.get("cost_pressure",.5),complexity=obj.get("complexity",.5))
            BREAKER.success();tr.add("optimize.success")
            out["trace"]=tr.finish()
            if idem:IDEMP.put(tenant+":"+idem,out)
            return self._json(200,out)
        except Exception as e:
            BREAKER.failure();tr.add("optimize.error",error=str(e));return self._json(500,{"error":str(e),"trace":tr.finish()})
        finally:QUOTA.release(tenant)
    def log_message(self,*args):pass

def run(port=8787):
    print(f"TopoSpace distributed server on :{port}")
    ThreadingHTTPServer(("0.0.0.0",port),Handler).serve_forever()
if __name__=="__main__":run(int(os.getenv("PORT","8787")))
