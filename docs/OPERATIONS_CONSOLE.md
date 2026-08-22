
# TopoSpace v3.2 Operations Console

The console is an operational surface over the framework-agnostic runtime. It shows:
- request volume and p95 latency
- optimized context token usage
- recent optimization events
- live task/context/memory/tool topology
- tenant-scoped observability

The console event model is intentionally compatible with TorusDB Agent Memory nodes so the memory
topology can be merged into the same graph without making TorusDB a hard dependency.
