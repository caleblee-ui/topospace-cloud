
from __future__ import annotations
from middleware.hooks import AgentMiddleware,HookResult,ToolCallEnvelope
from production.adaptive_engine import AdaptiveTopoSpaceEngine
from torusdb.bridge import TorusTopoMemoryBridge

class TopoSpaceMiddleware(AgentMiddleware):
    """Framework-agnostic middleware for any agent loop."""
    def __init__(self,engine=None,memory_bridge:TorusTopoMemoryBridge|None=None):
        self.engine=engine or AdaptiveTopoSpaceEngine()
        self.memory_bridge=memory_bridge

    def before_inference(self,envelope):
        combined=[]
        combined.extend(envelope.context or [])
        combined.extend(envelope.memories or [])

        plan=self.engine.optimize_adaptive(
            objective=envelope.objective,
            context=combined,
            agents=envelope.agents or [],
            required_capabilities=envelope.metadata.get("required_capabilities",[]),
            uncertainty=envelope.uncertainty,
            drift=envelope.drift,
            previous_success=envelope.previous_success,
            cost_pressure=envelope.cost_pressure,
            complexity=envelope.complexity,
        )

        envelope.context=plan.get("context",[])
        envelope.agents=plan.get("team",[])
        envelope.metadata["topospace_plan"]={
            "context_tokens":plan.get("context_tokens",0),
            "adaptive":plan.get("adaptive",{}),
            "quality_guard":plan.get("quality_guard",{}),
            "expanded_for_quality":plan.get("expanded_for_quality",False)
        }
        return HookResult(True,envelope,envelope.metadata["topospace_plan"])

    def before_tool(self,envelope,tool_call:ToolCallEnvelope):
        allowed_types=set(envelope.metadata.get("allowed_tool_types",[]))
        denied=set(envelope.metadata.get("denied_tools",[]))
        if tool_call.tool_name in denied:
            return HookResult(False,tool_call,{"reason":"tool_denied"})
        if allowed_types:
            typ=tool_call.metadata.get("type")
            if typ and typ not in allowed_types:
                return HookResult(False,tool_call,{"reason":"tool_type_not_allowed"})
        return HookResult(True,tool_call)

    def memory_recall(self,envelope,query):
        if not self.memory_bridge:
            return HookResult(True,[])
        out=self.memory_bridge.recall(
            query,
            limit=int(envelope.metadata.get("memory_candidate_limit",50)),
            max_return=int(envelope.metadata.get("memory_return_limit",12)),
            uncertainty=envelope.uncertainty,
            complexity=envelope.complexity,
            cost_pressure=envelope.cost_pressure
        )
        return HookResult(True,out.get("memories",[]),out)

    def state_update(self,envelope,event):
        if event.get("type")=="failure":
            envelope.previous_success=False
            envelope.uncertainty=min(1.0,max(envelope.uncertainty,float(event.get("uncertainty",.7))))
        if "drift" in event:
            envelope.drift=max(envelope.drift,float(event["drift"]))
        return HookResult(True,event,{"uncertainty":envelope.uncertainty,"drift":envelope.drift})
