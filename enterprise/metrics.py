
from collections import defaultdict
import threading,time

class MetricsRegistry:
    def __init__(self):
        self.counters=defaultdict(float);self.gauges={};self.lock=threading.RLock()

    def inc(self,name,value=1,labels=None):
        key=self._key(name,labels)
        with self.lock:self.counters[key]+=value

    def set(self,name,value,labels=None):
        key=self._key(name,labels)
        with self.lock:self.gauges[key]=float(value)

    @staticmethod
    def _key(name,labels):
        if not labels:return name
        suffix=",".join(f'{k}="{v}"' for k,v in sorted(labels.items()))
        return f"{name}{{{suffix}}}"

    def prometheus(self):
        lines=[]
        with self.lock:
            for k,v in sorted(self.counters.items()):lines.append(f"{k} {v}")
            for k,v in sorted(self.gauges.items()):lines.append(f"{k} {v}")
        return "\n".join(lines)+"\n"
