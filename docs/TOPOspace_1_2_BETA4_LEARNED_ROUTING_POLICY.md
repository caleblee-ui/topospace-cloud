
# TopoSpace 1.2 beta4 — Learned Model Routing Policy

beta4 connects execution telemetry back into model routing. Model utility is learned separately for low,
medium and high topology classes from observed quality, cost, latency and success. Conservative model-profile
priors are retained until enough observations exist.

A deterministic SafeRoutingPolicy remains outside the learned layer and can override learned choices for
high-risk workloads. The included benchmark is constructed synthetic ground truth for regression only.
Live provider A/B telemetry is required for commercial quality or savings claims.
