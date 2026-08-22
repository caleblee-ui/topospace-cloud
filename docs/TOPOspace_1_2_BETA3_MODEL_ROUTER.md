
# TopoSpace 1.2 beta3 — Topology-Aware Model Router

The gateway no longer needs to choose a logical model class from only risk/latency rules. beta3 introduces
a topology-aware model score using:

- task risk and ambiguity,
- topology complexity,
- cross-domain coupling strength,
- expected context size,
- expected tool calls,
- model quality / latency / cost profiles,
- historical model reward and success.

The routing layer is provider neutral. Deployment configuration can map logical model profiles to concrete
providers and models. The router also enforces per-model context limits before ranking candidates.

This is an execution optimization layer, not a claim that one model is universally superior. Real production
routing policy should be calibrated using actual provider A/B telemetry from TopoSpace 1.2 beta1.
