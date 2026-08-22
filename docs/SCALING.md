
# Scaling TopoSpace

v2.2 introduces interfaces and reference components for multi-tenant distributed deployment:
tenant quotas, request rate/concurrency limiting, circuit breaking, idempotency, worker queues,
request traces, rolling configuration, and distributed-state adapters.

Reference in-memory implementations are provided for tests/single-node deployments. Production
multi-node deployments should bind these interfaces to Redis/PostgreSQL/Kafka or equivalent managed
infrastructure.
