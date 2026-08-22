from dataclasses import dataclass
API_VERSION="v1";SCHEMA_VERSION="1.2"
@dataclass(frozen=True)
class GADecisionContract:
    model:str;geometry_family:str;execution_path:str;token_budget:int
    api_version:str=API_VERSION;schema_version:str=SCHEMA_VERSION
