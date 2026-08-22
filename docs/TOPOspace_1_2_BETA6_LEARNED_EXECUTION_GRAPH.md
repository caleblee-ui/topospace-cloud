
# TopoSpace 1.2 beta6 — Learned Execution Graph Policy

beta6 learns which execution path works best for each topology class instead of using only fixed escalation rules.

Reference path templates include:

- fast_only
- fast -> tool
- memory -> balanced
- balanced -> tool
- balanced -> reasoning
- memory -> balanced -> reasoning

The policy learns topology-conditioned utility from observed reward, success, cost and latency. A path compiler
turns the selected template into an executable graph. Safety constraints remain external to the learned utility:
high-risk tasks can forbid fast-only paths or require a reasoning stage.

This creates a hierarchy of optimization:

    topology -> model/path policy -> executable graph -> telemetry -> learned path utility

The included benchmark uses constructed ground truth solely to validate learning behavior. Real execution-path
or cost claims require live workloads.
