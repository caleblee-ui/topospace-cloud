from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class TopoObject:
    id: str
    type: str
    features: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
