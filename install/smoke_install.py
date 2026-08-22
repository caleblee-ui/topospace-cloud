
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from install.doctor import doctor
if __name__=="__main__":
    root=Path(__file__).resolve().parents[1]
    out=doctor(root);print(json.dumps(out,indent=2));raise SystemExit(0 if out["ok"] else 1)
