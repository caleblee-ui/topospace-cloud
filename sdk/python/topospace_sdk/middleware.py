
class RemoteTopoSpaceMiddleware:
    """Remote middleware helper using TopoSpaceClient."""
    def __init__(self,client):
        self.client=client

    def optimize(self,envelope):
        return self.client.optimize(
            objective=envelope.get("objective",""),
            context=envelope.get("context",[])+envelope.get("memories",[]),
            agents=envelope.get("agents",[]),
            required_capabilities=envelope.get("required_capabilities",[]),
            uncertainty=envelope.get("uncertainty",.3),
            drift=envelope.get("drift",0),
            previous_success=envelope.get("previous_success",True),
            cost_pressure=envelope.get("cost_pressure",.5),
            complexity=envelope.get("complexity",.5)
        )
