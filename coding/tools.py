from __future__ import annotations
from pathlib import Path
import subprocess, sys

class CodingTools:
    def __init__(self, root): self.root=Path(root); self.read_count=0; self.tool_calls=0
    def read(self,path):
        self.tool_calls+=1; self.read_count+=1
        return (self.root/path).read_text(errors='ignore')
    def patch_reference(self,path,task):
        self.tool_calls+=1; p=self.root/path; text=p.read_text()
        # Safe deterministic demo transformation for fixture: replace insecure compare marker.
        if 'INSECURE_TOKEN_COMPARE' in text:
            text=text.replace('return token == expected  # INSECURE_TOKEN_COMPARE','return __import__("hmac").compare_digest(token, expected)  # TOPOSPACE_PATCH')
            p.write_text(text); return True
        return False
    def test(self):
        self.tool_calls+=1
        p=subprocess.run([sys.executable,'-m','pytest','-q'],cwd=self.root,capture_output=True,text=True,timeout=30)
        return p.returncode,p.stdout+p.stderr
