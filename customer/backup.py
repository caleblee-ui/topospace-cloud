
from __future__ import annotations
from pathlib import Path
import tarfile,json,time,hashlib

class BackupManager:
    def create(self,output_path,files,metadata=None):
        output_path=Path(output_path)
        manifest={"created_at":time.time(),"files":[],"metadata":metadata or {}}
        with tarfile.open(output_path,"w:gz") as tar:
            for p in map(Path,files):
                if not p.exists(): continue
                data=p.read_bytes()
                manifest["files"].append({"name":p.name,"sha256":hashlib.sha256(data).hexdigest(),"size":len(data)})
                tar.add(p,arcname="data/"+p.name)
            m=json.dumps(manifest,sort_keys=True,indent=2).encode()
            info=tarfile.TarInfo("manifest.json");info.size=len(m)
            import io
            tar.addfile(info,io.BytesIO(m))
        return manifest

    def inspect(self,backup_path):
        with tarfile.open(backup_path,"r:gz") as tar:
            return json.loads(tar.extractfile("manifest.json").read())

    def restore(self,backup_path,destination):
        destination=Path(destination);destination.mkdir(parents=True,exist_ok=True)
        with tarfile.open(backup_path,"r:gz") as tar:
            members=[m for m in tar.getmembers() if m.name.startswith("data/") and ".." not in Path(m.name).parts]
            tar.extractall(destination,members=members)
        return destination
