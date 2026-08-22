
from pathlib import Path
import json

class GAReadiness:
    def __init__(self,root):
        self.root=Path(root)

    def checks(self):
        required=[
          "joint_optimizer",
          "online_learning",
          "runtime_server",
          "runtime_sdk",
          "general_geometry",
          "geometry_policy",
          "learned_field",
          "coupled_geometry",
        ]
        checks={name:(self.root/name).exists() for name in required}
        checks["v1_contract"]=(self.root/"contracts/v1-ga-contract.json").exists() or (self.root/"contracts/v1-frozen-contract.json").exists()
        checks["docker"]=(self.root/"deploy/docker/Dockerfile").exists() or (self.root/"deploy/beta/Dockerfile").exists()
        return {"ok":all(checks.values()),"checks":checks}
