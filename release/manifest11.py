
from pathlib import Path
import hashlib,time

def build_manifest(root,version):
    root=Path(root)
    files=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or ".pytest_cache" in p.parts:continue
        data=p.read_bytes()
        files.append({
          "path":str(p.relative_to(root)),
          "sha256":hashlib.sha256(data).hexdigest(),
          "size":len(data)
        })
    return {
      "product":"TopoSpace",
      "version":version,
      "status":"GA",
      "api_version":"v1",
      "generated_at":time.time(),
      "files":files
    }
