
from pathlib import Path
import hashlib,json,time

def build_release_manifest(root,version):
    root=Path(root)
    files=[]
    for p in sorted(root.rglob("*")):
        if not p.is_file() or "__pycache__" in p.parts or ".pytest_cache" in p.parts:continue
        data=p.read_bytes()
        files.append({"path":str(p.relative_to(root)),"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)})
    return {
      "product":"TopoSpace",
      "version":version,
      "status":"GA",
      "generated_at":time.time(),
      "api_contract":"v1",
      "files":files
    }
