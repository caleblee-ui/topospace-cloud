
from pathlib import Path
import hashlib,time
def build_sbom(root,version):
    root=Path(root);components=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or ".pytest_cache" in p.parts:continue
        components.append({
          "type":"file",
          "name":str(p.relative_to(root)),
          "version":version,
          "hashes":[{"alg":"SHA-256","content":hashlib.sha256(p.read_bytes()).hexdigest()}]
        })
    return {
      "bomFormat":"CycloneDX",
      "specVersion":"1.5",
      "metadata":{"timestamp":time.time(),"component":{"type":"application","name":"TopoSpace","version":version}},
      "components":components
    }
