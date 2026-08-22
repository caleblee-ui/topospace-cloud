
# Self-Optimizing Autopilot

v3.4 adds a learning layer above the bounded v3.3 controller:
- contextual UCB bandit chooses conservative/balanced/efficient operating profiles
- a dependency-free local surrogate search records promising continuous configurations
- a constrained objective rewards token/cost reduction only when success, latency and risk guardrails remain feasible

The deterministic safety controller remains authoritative. Learned profiles scale its outputs rather than
bypassing the operating envelope.
