
# Topological Multi-Agent Consensus Runtime

TopoSpace alpha7 allows agents with different local topologies to propose candidate Memory, Tool, Agent or
execution-path nodes for the same task. Consensus aggregates confidence, utility, topological proximity,
evidence and diversity of independent support.

A proposal does not win merely because one agent scores it highly. The negotiator requires sufficient
support and score; otherwise the runtime returns `needs_exploration`, allowing the system to widen epsilon,
query another agent, recall more memory or inspect another tool neighborhood.

This extends Collective Topology from knowledge sharing to cooperative execution-path selection.
