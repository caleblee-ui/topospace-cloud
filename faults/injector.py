
import random,time
class FaultInjector:
    def __init__(self,seed=71): self.rng=random.Random(seed)
    def maybe_fail(self,rate=.0,message="injected_failure"):
        if self.rng.random()<rate: raise RuntimeError(message)
    def maybe_delay(self,rate=.0,min_ms=1,max_ms=20):
        if self.rng.random()<rate:
            d=self.rng.uniform(min_ms,max_ms)/1000;time.sleep(d);return d*1000
        return 0.0
