import time
class HealthRegistry:
    def __init__(self): self.checks={}
    def register(self,name,fn): self.checks[name]=fn
    def snapshot(self):
        out={};ok=True
        for name,fn in self.checks.items():
            try:
                r=fn(); passed=bool(r if isinstance(r,bool) else r.get("ok",True)); out[name]=r if isinstance(r,dict) else {"ok":passed}; ok=ok and passed
            except Exception as e: out[name]={"ok":False,"error":str(e)};ok=False
        return {"ok":ok,"checks":out,"ts":time.time()}
