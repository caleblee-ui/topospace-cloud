
from __future__ import annotations
import json, urllib.request, urllib.parse
from torusdb.backend import TorusMemoryBackend
from torusdb.models import MemoryRecord

class TorusDBHTTPBackend(TorusMemoryBackend):
    """Configurable HTTP adapter.

    Default routes are reference contracts, not assumptions about an existing TorusDB API.
    Override route_map to match the deployed Agent Memory service.
    """
    def __init__(self,base_url,api_key=None,route_map=None):
        self.base_url=base_url.rstrip("/")
        self.api_key=api_key
        self.routes={
          "upsert":"/v1/memory/upsert",
          "get":"/v1/memory/{id}",
          "search":"/v1/memory/search",
          "delete":"/v1/memory/{id}",
        }
        self.routes.update(route_map or {})

    def _request(self,method,path,payload=None):
        headers={"content-type":"application/json"}
        if self.api_key: headers["authorization"]="Bearer "+self.api_key
        data=None if payload is None else json.dumps(payload).encode()
        req=urllib.request.Request(self.base_url+path,data=data,headers=headers,method=method)
        with urllib.request.urlopen(req,timeout=30) as r:
            raw=r.read()
            return json.loads(raw) if raw else None

    def upsert(self,record):
        obj=self._request("POST",self.routes["upsert"],record.payload())
        return MemoryRecord(**(obj.get("memory",obj) if obj else record.payload()))

    def get(self,memory_id):
        obj=self._request("GET",self.routes["get"].format(id=urllib.parse.quote(memory_id,safe="")))
        return None if not obj else MemoryRecord(**obj.get("memory",obj))

    def search(self,query,limit=50,filters=None):
        obj=self._request("POST",self.routes["search"],{"query":query,"limit":limit,"filters":filters or {}})
        rows=(obj or {}).get("memories",obj or [])
        return [MemoryRecord(**x) for x in rows]

    def delete(self,memory_id):
        obj=self._request("DELETE",self.routes["delete"].format(id=urllib.parse.quote(memory_id,safe="")))
        return bool((obj or {}).get("ok",True))
