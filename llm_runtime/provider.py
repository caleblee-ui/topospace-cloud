
from abc import ABC,abstractmethod
class LLMProvider(ABC):
    @abstractmethod
    def invoke(self,request,context=None,tools=None): ...
