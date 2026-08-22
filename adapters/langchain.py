
class LangChainTopoSpaceAdapter:
    """
    Optional thin bridge only. TopoSpace does not depend on LangChain.
    Wraps middleware as a retriever/tool-selection preprocessor.
    """
    def __init__(self,middleware): self.middleware=middleware
    def preprocess(self,request,spaces,state=None):
        return self.middleware.optimize(request,spaces,state)
