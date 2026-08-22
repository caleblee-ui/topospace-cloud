"""Dependency-free TopoSpace HTTP/SSE API.
GET /health, /objects, /traces, /events
POST /context
"""
from __future__ import annotations
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from runtime.events import sse_encode

class TopoSpaceHTTPHandler(BaseHTTPRequestHandler):
    runtime=None; event_bus=None
    def _send(self,code,obj):
        body=json.dumps(obj).encode();self.send_response(code);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(body)));self.send_header('Access-Control-Allow-Origin','*');self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/objects':return self._send(200,[{'id':o.id,'type':o.type,'features':o.features,'metadata':o.metadata} for o in self.runtime.space.objects()])
        if self.path=='/traces':return self._send(200,self.runtime.export_trace())
        if self.path=='/health':return self._send(200,{'status':'ok','service':'topospace','streaming':self.event_bus is not None})
        if self.path=='/events' and self.event_bus is not None:
            self.send_response(200);self.send_header('Content-Type','text/event-stream');self.send_header('Cache-Control','no-cache');self.send_header('Connection','keep-alive');self.send_header('Access-Control-Allow-Origin','*');self.end_headers()
            try:
                for item in self.event_bus.subscribe():
                    self.wfile.write(sse_encode(item).encode());self.wfile.flush()
            except (BrokenPipeError,ConnectionResetError):pass
            return
        return self._send(404,{'error':'not found'})
    def do_POST(self):
        n=int(self.headers.get('Content-Length','0'));data=json.loads(self.rfile.read(n) or b'{}')
        if self.path!='/context':return self._send(404,{'error':'not found'})
        state=self.runtime.space.get(data['state_id'])
        if not state:return self._send(404,{'error':'state not found'})
        b=self.runtime.context(state,data.get('objective',''),object_types=data.get('object_types'),max_points=int(data.get('max_points',32)),epsilon=data.get('epsilon'))
        return self._send(200,b.to_dict())
    def log_message(self,*args):pass

def serve(runtime,host='127.0.0.1',port=8765,event_bus=None):
    cls=type('BoundTopoSpaceHTTPHandler',(TopoSpaceHTTPHandler,),{'runtime':runtime,'event_bus':event_bus})
    server=ThreadingHTTPServer((host,port),cls);print(f'TopoSpace HTTP listening on http://{host}:{port}');server.serve_forever()
