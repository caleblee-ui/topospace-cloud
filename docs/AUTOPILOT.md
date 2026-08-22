
# Topology Autopilot

TopoSpace v3.3 automatically adjusts:
- epsilon neighborhood radius
- weighted-Lp exponent
- context token budget
- TorusDB memory recall depth
- tool neighborhood radius
- exploration level

Inputs are runtime feedback rather than model-provider specifics:
success rate, uncertainty, topology drift, token pressure, latency pressure, tool failure rate and memory hit rate.

A safety policy limits parameter movement between consecutive control steps so the optimizer cannot make
unbounded changes from a single noisy observation.
