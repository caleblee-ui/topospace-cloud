
from torusdb.memory_backend import InMemoryTorusBackend
from torusdb.models import MemoryRecord
from torusdb.bridge import TorusTopoMemoryBridge
from middleware.topospace_middleware import TopoSpaceMiddleware
from middleware.hooks import AgentEnvelope

class TorusMemoryE2E:
    def __init__(self):
        self.backend=InMemoryTorusBackend()
        self.bridge=TorusTopoMemoryBridge(self.backend)
        self.middleware=TopoSpaceMiddleware(memory_bridge=self.bridge)

    def run(self):
        self.backend.upsert(MemoryRecord("auth-decision","oauth refresh token design",semantic_score=.95,importance=.9,distance=.08,tokens=120))
        self.backend.upsert(MemoryRecord("ui-note","button spacing",semantic_score=.1,importance=.2,distance=.8,tokens=80))
        env=AgentEnvelope("oauth refresh token issue",uncertainty=.25,complexity=.4,cost_pressure=.7)
        recalled=self.middleware.memory_recall(env,"oauth refresh token")
        env.memories=recalled.payload
        pre=self.middleware.before_inference(env)
        return {"recalled":[x["id"] for x in recalled.payload],"visible":[x["id"] for x in pre.payload.context]}
