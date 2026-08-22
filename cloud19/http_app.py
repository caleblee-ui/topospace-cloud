
"""
Minimal ASGI application without framework lock-in.
POST /v1/chat/completions accepts an OpenAI-style message/model/max_tokens payload
and returns a TopoSpace optimized execution plan. A provider adapter can execute it.
"""
import json
from cloud19.openai_compat import ChatCompletionRequest
class TopoSpaceASGI:
    def __init__(self,service):self.service=service
    async def __call__(self,scope,receive,send):
        if scope["type"]!="http":return
        if scope["path"]!="/v1/chat/completions" or scope["method"]!="POST":
            await send({"type":"http.response.start","status":404,"headers":[]});await send({"type":"http.response.body","body":b"not found"});return
        body=b""
        while True:
            m=await receive();body+=m.get("body",b"")
            if not m.get("more_body"):break
        headers={k.decode().lower():v.decode() for k,v in scope.get("headers",[])}
        key=headers.get("authorization","").removeprefix("Bearer ").strip()
        try:
            data=json.loads(body or b"{}");req=ChatCompletionRequest(data.get("messages",[]),data.get("model","auto"),data.get("max_tokens",1024),data.get("metadata",{}))
            out=self.service.chat_completions(key,req,data.get("topospace_state",{}));payload=json.dumps(out).encode();status=200
        except PermissionError as e:payload=json.dumps({"error":str(e)}).encode();status=401
        except RuntimeError as e:payload=json.dumps({"error":str(e)}).encode();status=429
        except Exception as e:payload=json.dumps({"error":"bad_request"}).encode();status=400
        await send({"type":"http.response.start","status":status,"headers":[(b"content-type",b"application/json")]})
        await send({"type":"http.response.body","body":payload})
