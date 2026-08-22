
import sys,sqlite3,ssl
from pathlib import Path
def doctor(root):
    root=Path(root)
    checks={
      "python":sys.version_info>=(3,10),
      "sqlite":sqlite3.sqlite_version_info>=(3,35,0),
      "ssl":bool(ssl.OPENSSL_VERSION),
      "commercial_api":(root/"server/commercial_app.py").exists(),
      "middleware":(root/"middleware/topospace_middleware.py").exists(),
      "torusdb_bridge":(root/"torusdb/bridge.py").exists(),
      "helm":(root/"deploy/helm/topospace/Chart.yaml").exists(),
    }
    return {"ok":all(checks.values()),"checks":checks}
