
import json
from cloud19.openai_compat import ChatCompletionRequest
from cloud20.sse import encode_sse

class ProductionASGI:
    def __init__(self,service):self.service=service

    async def _response(self,send,status,obj,content_type=b"application/json"):
        body=json.dumps(obj).encode()
        await send({"type":"http.response.start","status":status,"headers":[(b"content-type",content_type)]})
        await send({"type":"http.response.body","body":body})

    async def __call__(self,scope,receive,send):
        if scope["type"]!="http":return
        path=scope.get("path","")
        method=scope.get("method","GET")
        if path in {"/health","/healthz"}:
            return await self._response(send,200,{"ok":True,"service":"topospace-cloud"})
        if path=="/":
            return await self._response(send,200,{"name":"TopoSpace Cloud","version":"1.3.0-beta1","api":"/v1/chat/completions"})
        if path!="/v1/chat/completions" or method!="POST":
            return await self._response(send,404,{"error":"not_found"})

        body=b""
        while True:
            m=await receive();body+=m.get("body",b"")
            if not m.get("more_body"):break
        headers={k.decode().lower():v.decode() for k,v in scope.get("headers",[])}
        key=headers.get("authorization","").removeprefix("Bearer ").strip()
        try:
            data=json.loads(body or b"{}")
            req=ChatCompletionRequest(
                data.get("messages",[]),
                data.get("model","auto"),
                data.get("max_tokens",1024),
                data.get("metadata",{})
            )
            state=data.get("topospace_state",{})
            if data.get("stream",False):
                await send({"type":"http.response.start","status":200,"headers":[(b"content-type",b"text/event-stream"),(b"cache-control",b"no-cache")]})
                for e in self.service.stream_chat(key,req,state):
                    await send({"type":"http.response.body","body":encode_sse(e["event"],e["data"]),"more_body":True})
                await send({"type":"http.response.body","body":b"data: [DONE]\n\n","more_body":False})
                return
            out=self.service.execute_chat(key,req,state)
            return await self._response(send,200,out)
        except PermissionError as e:
            return await self._response(send,401,{"error":str(e)})
        except RuntimeError as e:
            msg=str(e)
            status=429 if msg in {"rate_limit_exceeded","quota_exceeded"} else 502
            return await self._response(send,status,{"error":msg})
        except Exception:
            return await self._response(send,400,{"error":"bad_request"})
