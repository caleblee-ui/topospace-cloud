class CommercialResponse:
    def __init__(self,payload):
        self.payload=payload;self.request_id=payload.get("request_id");self.result=payload.get("result",{});self.latency_ms=payload.get("latency_ms",0);self.engine_version=payload.get("engine_version")
    @property
    def context(self):return self.result.get("context",[])
    @property
    def team(self):return self.result.get("team",[])
