
from __future__ import annotations
from pathlib import Path
import hashlib,json,time

class SBOMBuilder:
    """Creates a lightweight CycloneDX-like inventory for bundled source artifacts."""
    def build(self,root):
        root=Path(root)
        components=[]
        for p in sorted(root.rglob("*")):
            if not p.is_file() or "__pycache__" in p.parts or ".pytest_cache" in p.parts:continue
            data=p.read_bytes()
            components.append({
              "name":str(p.relative_to(root)),
              "type":"file",
              "hashes":[{"alg":"SHA-256","content":hashlib.sha256(data).hexdigest()}],
              "size":len(data)
            })
        return {
          "bomFormat":"CycloneDX",
          "specVersion":"1.5",
          "serialNumber":"urn:uuid:topospace-local",
          "metadata":{"timestamp":time.time(),"component":{"name":"topospace","type":"application"}},
          "components":components
        }
