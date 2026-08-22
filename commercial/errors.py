from dataclasses import dataclass
@dataclass
class TopoSpaceError(Exception):
    code:str; message:str; retryable:bool=False; status:int=500
    def to_dict(self): return {"error":{"code":self.code,"message":self.message,"retryable":self.retryable}}
