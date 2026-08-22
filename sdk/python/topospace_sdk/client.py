
import json,urllib.request
class TopoSpaceClient:
    def __init__(self,base_url="http://localhost:8787",key_id=None,key=None):
        self.base_url=base_url.rstrip("/");self.key_id=key_id;self.key=key
    def optimize(self,**payload):
        headers={"content-type":"application/json"}
        if self.key_id:headers["x-topospace-key-id"]=self.key_id
        if self.key:headers["x-topospace-key"]=self.key
        req=urllib.request.Request(self.base_url+"/v1/optimize",data=json.dumps(payload).encode(),headers=headers,method="POST")
        with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())
    def health(self):
        with urllib.request.urlopen(self.base_url+"/health",timeout=10) as r:return json.loads(r.read())
