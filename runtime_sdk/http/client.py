
from __future__ import annotations
import json,urllib.request

class TopoSpaceRuntimeHTTPClient:
    def __init__(self,base_url,tenant_id="default",project_id="default",agent_id="agent",key_id=None,key=None):
        self.base_url=base_url.rstrip("/")
        self.headers={
          "content-type":"application/json",
          "x-topospace-tenant":tenant_id,
          "x-topospace-project":project_id,
          "x-topospace-agent":agent_id
        }
        if key_id:self.headers["x-topospace-key-id"]=key_id
        if key:self.headers["x-topospace-key"]=key

    def dispatch(self,hook,task_id,**payload):
        body=json.dumps({"task_id":task_id,**payload}).encode()
        req=urllib.request.Request(self.base_url+"/v1/runtime/"+hook,data=body,headers=self.headers,method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())

    def snapshot(self):
        req=urllib.request.Request(self.base_url+"/v1/runtime/snapshot",headers=self.headers,method="GET")
        with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())
