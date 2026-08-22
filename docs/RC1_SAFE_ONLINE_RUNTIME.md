
# TopoSpace 1.1.0-rc1 — Safe Online Joint Optimization Runtime

rc1 operationalizes the Joint Geometry Optimizer in a production-style learning loop:

1. Champion policy serves live traffic.
2. Challenger policy runs the same task in shadow.
3. Offline/shadow evidence accumulates.
4. Promotion requires reward gain, sample sufficiency, success preservation, zero policy/security violations,
   and bounded latency regression.
5. Approved challengers enter staged rollout: 5% -> 25% -> 50% -> 100%.
6. Runtime health is continuously checked for reward, error, latency and violation regressions.
7. Automatic rollback returns traffic to the prior champion when guardrails fail.

This layer is intentionally separate from the mathematical optimizer: the optimizer learns topology, while
PolicyOps decides whether a learned topology is safe enough to influence production traffic.
