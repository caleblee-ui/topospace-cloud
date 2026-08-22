
# TopoSpace Runtime SDK

TopoSpace alpha8 exposes the topological engine as framework-agnostic middleware rather than requiring an
application to adopt a specific agent framework.

Integration is based on lifecycle hooks:

`task_start → memory_recall → before_model → after_model → before_tool → after_tool → task_complete`

The application keeps control of its model and tool execution. TopoSpace observes and transforms the execution
space around those calls: cognitive memory recall, topology projection, outcome learning, consolidation,
collective sharing and consensus can remain middleware concerns.

This makes the architecture compatible in principle with custom agent loops and adapter-based integrations
for third-party frameworks without making those frameworks a dependency of the core runtime.
