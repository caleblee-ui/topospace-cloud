
from dataclasses import dataclass
import os

@dataclass(frozen=True)
class ProductionEnvironment:
    port:int=8787
    environment:str="production"
    log_level:str="INFO"
    torusdb_url:str|None=None
    torusdb_api_key:str|None=None
    redis_url:str|None=None
    postgres_dsn:str|None=None
    require_mtls:bool=False
    api_key_id:str|None=None
    api_key_secret:str|None=None

    @classmethod
    def from_env(cls):
        truth=lambda x:str(x).lower() in {"1","true","yes","on"}
        return cls(
          port=int(os.getenv("PORT","8787")),
          environment=os.getenv("TOPOSPACE_ENV","production"),
          log_level=os.getenv("TOPOSPACE_LOG_LEVEL","INFO"),
          torusdb_url=os.getenv("TORUSDB_URL"),
          torusdb_api_key=os.getenv("TORUSDB_API_KEY"),
          redis_url=os.getenv("REDIS_URL"),
          postgres_dsn=os.getenv("POSTGRES_DSN"),
          require_mtls=truth(os.getenv("TOPOSPACE_REQUIRE_MTLS","false")),
          api_key_id=os.getenv("TOPOSPACE_API_KEY_ID"),
          api_key_secret=os.getenv("TOPOSPACE_API_KEY_SECRET"),
        )

    def validate(self):
        errors=[]
        if not (1<=self.port<=65535):errors.append("invalid_port")
        if self.environment=="production" and bool(self.api_key_id)!=bool(self.api_key_secret):
            errors.append("partial_api_key_configuration")
        return {"ok":not errors,"errors":errors}
