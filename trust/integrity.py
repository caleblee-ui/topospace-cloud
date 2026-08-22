
from __future__ import annotations
from pathlib import Path
import hashlib,json

class RuntimeIntegrityVerifier:
    def manifest(self,root):
        root=Path(root);out={}
        for p in sorted(root.rglob("*.py")):
            if "__pycache__" in p.parts:continue
            out[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
        return out

    def verify(self,root,manifest):
        current=self.manifest(root)
        missing=sorted(set(manifest)-set(current))
        added=sorted(set(current)-set(manifest))
        changed=sorted(k for k in set(manifest)&set(current) if manifest[k]!=current[k])
        return {"ok":not(missing or added or changed),"missing":missing,"added":added,"changed":changed}
