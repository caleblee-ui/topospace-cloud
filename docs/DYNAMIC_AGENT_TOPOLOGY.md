
# Dynamic Agent Topology

TopoSpace now treats Task, Agent, Tool, Memory and Context as runtime nodes in a changing topological graph.

The graph is not merely visualization. It is an execution substrate:
- task ↔ memory: recall
- memory ↔ context: compilation
- task ↔ tool: capability requirement
- task ↔ agent: delegation
- agent ↔ tool: invocation

Runtime outcomes update node scores and therefore alter subsequent neighborhoods and execution paths.
The browser component renders the same node/edge model used by the planner, enabling an operator to inspect
which neighborhood the runtime explored and why a node was selected.
