
import time,threading
class CircuitBreaker:
    def __init__(self,failure_threshold=5,recovery_seconds=30):
        self.failure_threshold=failure_threshold;self.recovery_seconds=recovery_seconds
        self.failures=0;self.opened_at=None;self.lock=threading.RLock()
    def allow(self):
        with self.lock:
            if self.opened_at is None:return True
            if time.time()-self.opened_at>=self.recovery_seconds:
                self.failures=0;self.opened_at=None;return True
            return False
    def success(self):
        with self.lock:self.failures=0;self.opened_at=None
    def failure(self):
        with self.lock:
            self.failures+=1
            if self.failures>=self.failure_threshold:self.opened_at=time.time()
