
# TopoSpace 1.2.0-rc1 — Meta-Policy Production Runtime

rc1 integrates the 1.2 Meta-Policy Control Plane into a production-style runtime.

The live champion controls:
- generalized geometry,
- model selection,
- execution graph path.

A challenger evaluates the same topology in shadow. Promotion requires sufficient samples, reward improvement,
success preservation, zero policy/security violations and bounded latency regression. Approved challengers
progress through staged rollout and remain subject to automatic rollback.

This release also exposes a gateway bridge so the existing Agent Runtime Gateway can consume a single Meta-Policy
decision without requiring the application to understand the internal geometry/model/path policies separately.
