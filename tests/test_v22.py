
from production.quota import QuotaManager,TenantQuota
from production.circuit_breaker import CircuitBreaker
from production.idempotency import IdempotencyStore
from distributed.state import InMemoryDistributedState
from distributed.queue import WorkerQueue
from production.trace import RequestTrace

def test_quota():
 q=QuotaManager();q.set_quota("t",TenantQuota(requests_per_minute=1,max_concurrent=1))
 assert q.admit("t")["ok"];assert not q.admit("t")["ok"];q.release("t")

def test_breaker():
 b=CircuitBreaker(failure_threshold=2,recovery_seconds=999);assert b.allow();b.failure();b.failure();assert not b.allow()

def test_idempotency():
 s=IdempotencyStore();s.put("k",{"x":1});assert s.get("k")["x"]==1

def test_distributed_state():
 s=InMemoryDistributedState();s.set("a",1);assert s.get("a")==1;s.delete("a");assert s.get("a") is None

def test_worker_queue():
 q=WorkerQueue(workers=1);jid=q.submit(lambda x:x+1,2);q.q.join();assert q.get(jid)["result"]==3;q.shutdown()

def test_trace():
 t=RequestTrace("x");t.add("a");o=t.finish();assert o["trace_id"]=="x" and o["events"][0]["event"]=="a"
