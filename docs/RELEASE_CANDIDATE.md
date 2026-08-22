
# TopoSpace 1.0 Release Candidate

v3.8 freezes the public v1 optimize contract and validates the release candidate across:
- backward-compatible response contract
- upgrade/migration hooks
- 5k in-process soak test
- fault injection regression
- TorusDB Agent Memory end-to-end recall path
- installation doctor
- trust/integrity components
- RC readiness console

Before a true GA release, run the same suite against the actual production topology:
real Redis/PostgreSQL, real TorusDB deployment, TLS/mTLS ingress, enterprise identity, and at least one
external LLM/agent runtime under representative customer load.
