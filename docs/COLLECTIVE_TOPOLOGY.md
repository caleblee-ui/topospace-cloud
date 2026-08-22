
# Collective Topology Runtime

TopoSpace alpha6 introduces local and shared topological spaces for multi-agent systems.

Each agent keeps a local topology that preserves specialization. Successful local execution patterns and
semantic cognitive memories may be promoted to a tenant/global shared topology. Other agents do not blindly
inherit them: a knowledge broker ranks shared candidates against the receiving agent's specialization and scope.

This creates three layers of organization:
- Local topology: agent-specific state and specialization.
- Shared tenant topology: reusable memory, tool paths and execution patterns.
- Global topology: explicitly shareable patterns across tenants/environments.

The design keeps collective learning separate from forced synchronization, which makes it suitable for
framework-agnostic agent runtimes and TorusDB-backed durable memory.
