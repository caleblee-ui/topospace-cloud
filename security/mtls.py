
from dataclasses import dataclass

@dataclass
class MTLSConfig:
    enabled:bool=True
    ca_file:str|None=None
    cert_file:str|None=None
    key_file:str|None=None
    require_client_cert:bool=True

    def validate(self):
        if not self.enabled:return {"ok":True}
        missing=[x for x in ("ca_file","cert_file","key_file") if not getattr(self,x)]
        return {"ok":not missing,"missing":missing}
