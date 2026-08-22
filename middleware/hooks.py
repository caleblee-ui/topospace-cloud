
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass
class AgentEnvelope:
    objective: str
    messages: List[dict] = field(default_factory=list)
    context: List[dict] = field(default_factory=list)
    memories: List[dict] = field(default_factory=list)
    tools: List[dict] = field(default_factory=list)
    agents: List[dict] = field(default_factory=list)
    metadata: Dict[str,Any] = field(default_factory=dict)
    uncertainty: float = .3
    drift: float = 0.0
    complexity: float = .5
    cost_pressure: float = .5
    previous_success: bool = True

@dataclass
class ToolCallEnvelope:
    tool_name: str
    arguments: Dict[str,Any] = field(default_factory=dict)
    metadata: Dict[str,Any] = field(default_factory=dict)

@dataclass
class HookResult:
    allowed: bool = True
    payload: Any = None
    metadata: Dict[str,Any] = field(default_factory=dict)

class AgentMiddleware:
    def before_inference(self,envelope:AgentEnvelope)->HookResult:
        return HookResult(True,envelope)

    def after_inference(self,envelope:AgentEnvelope,model_result:Any)->HookResult:
        return HookResult(True,model_result)

    def before_tool(self,envelope:AgentEnvelope,tool_call:ToolCallEnvelope)->HookResult:
        return HookResult(True,tool_call)

    def after_tool(self,envelope:AgentEnvelope,tool_call:ToolCallEnvelope,tool_result:Any)->HookResult:
        return HookResult(True,tool_result)

    def memory_recall(self,envelope:AgentEnvelope,query:str)->HookResult:
        return HookResult(True,[])

    def state_update(self,envelope:AgentEnvelope,event:Dict[str,Any])->HookResult:
        return HookResult(True,event)
