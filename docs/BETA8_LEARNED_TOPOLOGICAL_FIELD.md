
# TopoSpace 1.1 beta8 — Learned Topological Field Runtime

beta8 replaces the fixed cross-domain coupling matrix with a state-conditioned field:

    C = C_theta(s)

The coupling strength between Memory, Tool, Skill and Planning spaces now depends on the current agent state:
risk, ambiguity, hierarchy, candidate pressure, latency pressure, memory pressure and tool pressure.

The field is not the local generalized distance itself. It modulates how the local geometries interact across
the product state space:

    X = X_memory × X_tool × X_skill × X_plan.

Reward feedback updates the coupling field, allowing repeated successful task families to strengthen useful
cross-domain paths such as Memory -> Plan or Tool -> Skill. Hard policy/security constraints remain outside
the compensatory field and continue to gate actionable candidates before routing.

This is the first TopoSpace version in which both local geometry and inter-domain topology are adaptive.
