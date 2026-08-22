
from abc import ABC,abstractmethod
from dataclasses import dataclass,field

@dataclass
class ProviderResponse:
    text:str
    model:str
    input_tokens:int=0
    output_tokens:int=0
    tool_calls:int=0
    latency_ms:float=0.0
    cost:float=0.0
    metadata:dict=field(default_factory=dict)

class ProviderAdapter(ABC):
    @abstractmethod
    def complete(self,model,messages,max_tokens,metadata=None):...
    def stream(self,model,messages,max_tokens,metadata=None):
        r=self.complete(model,messages,max_tokens,metadata)
        yield {"type":"message_start","model":r.model}
        yield {"type":"content_delta","delta":r.text}
        yield {"type":"message_end","usage":{"input_tokens":r.input_tokens,"output_tokens":r.output_tokens}}
