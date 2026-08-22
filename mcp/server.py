"""Minimal MCP-compatible stdio tool server using JSON-RPC 2.0.
Targets the stable 2025-11-25 core shape: initialize, tools/list, tools/call.
Kept deliberately small; production deployments should use an official MCP SDK.
"""
from __future__ import annotations
import json, sys

class MCPServer:
    def __init__(self,runtime): self.runtime=runtime
    def tools(self):
        schema={"type":"object","properties":{"state_id":{"type":"string"},"objective":{"type":"string"},"max_points":{"type":"integer"}},"required":["state_id"]}
        return [{"name":"topospace_context","description":"Build an adaptive topological context neighborhood for an AI state.","inputSchema":schema},
                {"name":"topospace_route_tools","description":"Route tools using the adaptive topological state space.","inputSchema":schema},
                {"name":"topospace_recall","description":"Recall memories from the adaptive topological neighborhood.","inputSchema":schema}]
    def call(self,name,args):
        s=self.runtime.space.get(args['state_id']); obj=args.get('objective',''); mp=int(args.get('max_points',32))
        if not s: raise ValueError('state not found')
        if name=='topospace_route_tools': b=self.runtime.route_tools(s,obj,max_points=mp)
        elif name=='topospace_recall': b=self.runtime.recall(s,obj,max_points=mp)
        else: b=self.runtime.context(s,obj,max_points=mp)
        return {"content":[{"type":"text","text":json.dumps(b.to_dict())}],"structuredContent":b.to_dict()}
    def handle(self,r):
        m=r.get('method'); rid=r.get('id')
        if m=='initialize': result={"protocolVersion":"2025-11-25","capabilities":{"tools":{}},"serverInfo":{"name":"topospace","version":"0.3.0"}}
        elif m=='notifications/initialized': return None
        elif m=='tools/list': result={"tools":self.tools()}
        elif m=='tools/call': result=self.call(r['params']['name'],r['params'].get('arguments',{}))
        else: return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}
        return {"jsonrpc":"2.0","id":rid,"result":result}
    def run_stdio(self):
        for line in sys.stdin:
            try:
                r=json.loads(line); out=self.handle(r)
                if out is not None: print(json.dumps(out),flush=True)
            except Exception as e:
                print(json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32603,"message":str(e)}}),flush=True)
