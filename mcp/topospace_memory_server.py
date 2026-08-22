
"""Dependency-light MCP JSON-RPC reference server.

Implements initialize, tools/list and tools/call over POST /mcp. For public production
submission, validate against the current MCP SDK/Inspector and deploy behind HTTPS/auth.
"""
from __future__ import annotations
import json,os
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from torusdb.memory_backend import InMemoryTorusBackend
from torusdb.http_backend import TorusDBHTTPBackend
from torusdb.bridge import TorusTopoMemoryBridge
from torusdb.models import MemoryRecord
from mcp.topospace_memory_tools import TOOLS

def make_backend():
    url=os.getenv("TORUSDB_URL")
    return TorusDBHTTPBackend(url,os.getenv("TORUSDB_API_KEY")) if url else InMemoryTorusBackend()

BRIDGE=TorusTopoMemoryBridge(make_backend())

def call_tool(name,args):
    if name=="topospace_memory_recall":
        return BRIDGE.recall(args["query"],int(args.get("limit",50)),int(args.get("max_return",12)))
    if name=="topospace_memory_get":
        x=BRIDGE.backend.get(args["memory_id"])
        return None if x is None else x.payload()
    if name=="topospace_memory_remember":
        rec=MemoryRecord(id=args["id"],content=args.get("content"),ciphertext=args.get("ciphertext"),
                         metadata=args.get("metadata",{}),tokens=int(args.get("tokens",0)))
        return BRIDGE.remember(rec).payload()
    if name=="topospace_memory_forget":
        return {"ok":BRIDGE.forget(args["memory_id"])}
    raise KeyError(name)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path!="/mcp": return self._reply(404,{"error":"not_found"})
        n=int(self.headers.get("content-length","0") or 0)
        req=json.loads(self.rfile.read(n) or b"{}")
        mid=req.get("id"); method=req.get("method"); params=req.get("params") or {}
        try:
            if method=="initialize":
                result={"protocolVersion":params.get("protocolVersion","2025-11-25"),
                        "capabilities":{"tools":{}},"serverInfo":{"name":"topospace-torus-memory","version":"2.6.0"}}
            elif method=="tools/list":
                result={"tools":TOOLS}
            elif method=="tools/call":
                out=call_tool(params["name"],params.get("arguments") or {})
                result={"content":[{"type":"text","text":json.dumps(out,ensure_ascii=False)}],"structuredContent":out}
            else: raise KeyError("method_not_found")
            return self._reply(200,{"jsonrpc":"2.0","id":mid,"result":result})
        except Exception as e:
            return self._reply(200,{"jsonrpc":"2.0","id":mid,"error":{"code":-32000,"message":str(e)}})

    def _reply(self,status,obj):
        body=json.dumps(obj).encode();self.send_response(status);self.send_header("content-type","application/json");self.send_header("content-length",str(len(body)));self.end_headers();self.wfile.write(body)
    def log_message(self,*args):pass

if __name__=="__main__":
    ThreadingHTTPServer(("0.0.0.0",int(os.getenv("PORT","8790"))),Handler).serve_forever()
