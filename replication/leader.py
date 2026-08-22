
import threading,time,uuid
class LeaderElection:
    """Reference lease-based leader election for single-process tests."""
    def __init__(self,lease_seconds=10):
        self.lease_seconds=lease_seconds;self.owner=None;self.expires=0;self.lock=threading.RLock()
    def acquire(self,node_id):
        with self.lock:
            now=time.time()
            if self.owner is None or now>=self.expires or self.owner==node_id:
                self.owner=node_id;self.expires=now+self.lease_seconds;return True
            return False
    def renew(self,node_id):
        return self.acquire(node_id)
    def current(self):
        with self.lock:
            if self.owner and time.time()<self.expires:return self.owner
            return None
