
# TopoSpace 1.1 beta5 — Geometry Policy Network

beta5 makes the generalized geometry itself adaptive.

Instead of learning only the exponent p and view weights, the runtime now selects a geometry family A_theta,
its view weights w_theta, exponent parameters where applicable, and the adaptive radius epsilon_theta.

    (s,g,runtime) -> Geometry Policy -> (A_theta, w_theta, p_theta, epsilon_theta)

The reference policy supports four operational families:
- Lp: compensatory evidence aggregation.
- Weighted Chebyshev: non-compensatory bottleneck geometry for policy/security.
- OWA: emphasizes the worst few views under candidate pressure.
- Nested: hierarchical composition, e.g. semantic L1 + policy max + operational L2.

The policy head contains explicit inductive priors rather than claiming that a tiny synthetic learner discovers
the full geometry from scratch. It can then be updated online using reward derived from retrieval quality,
constraint violations, latency and token cost.

This is deliberately a reference policy layer. Production deployment should replace the lightweight head with
a trained neural policy while retaining GeometryDecision and GeometryCompiler as stable runtime interfaces.
