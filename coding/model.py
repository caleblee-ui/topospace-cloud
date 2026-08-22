from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List

@dataclass
class AgentDecision:
    action: str
    path: str | None = None
    payload: str | None = None
    reason: str = ''

class ModelAdapter(ABC):
    @abstractmethod
    def decide(self, *, task: str, context: list, observations: list) -> AgentDecision: raise NotImplementedError

class ReferenceCodingModel(ModelAdapter):
    """Deterministic offline model for E2E validation. Production can plug in any LLM."""
    def decide(self, *, task, context, observations):
        paths=[getattr(x,'metadata',{}).get('path') for x in context]
        paths=[p for p in paths if p]
        if not observations:
            preferred=next((p for p in paths if 'auth' in p.lower()), paths[0] if paths else None)
            return AgentDecision('read',preferred,reason='inspect most relevant implementation')
        if not any(o.get('kind')=='patched' for o in observations):
            preferred=next((p for p in paths if p and 'auth' in p.lower()),paths[0] if paths else None)
            return AgentDecision('patch',preferred,payload='REFERENCE_PATCH',reason='apply task-specific reference patch')
        return AgentDecision('test',reason='validate repository after change')
