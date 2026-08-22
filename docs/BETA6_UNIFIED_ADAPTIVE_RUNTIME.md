
# TopoSpace 1.1 beta6 — Unified Adaptive Agent Runtime

beta6 connects the Geometry Policy Network to four runtime spaces at once:

- Memory recall
- Tool routing
- Skill routing
- Planning candidates

One shared policy chooses the operational geometry for each domain from the same agent/runtime state.
For actionable domains (Tool and Plan), hard policy/security views are enforced by a non-compensatory gate
before generalized geometry ranking. This avoids allowing a strong semantic match to compensate for a hard
constraint violation.

The selected geometry family, weights, p and epsilon determine each remaining neighborhood. The resulting
neighborhoods are composed into an execution bundle, and per-domain success/constraint/cost feedback updates
the geometry policy online.

This is the first version where generalized geometry is the common control plane for the agent's memory,
tool, skill and planning spaces.
