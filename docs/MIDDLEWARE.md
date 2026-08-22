
# Framework-Agnostic Middleware

TopoSpace is not coupled to LangChain, LangGraph, or any particular agent framework.

Primary integration surfaces:
1. Embedded Python middleware hooks
2. Remote REST middleware service
3. Python/TypeScript SDK
4. MCP for clients that prefer tool-based integration

Lifecycle hooks:
- memory_recall
- before_inference
- after_inference
- before_tool
- after_tool
- state_update

TorusDB can remain the durable Agent Memory backend while TopoSpace controls which memories become
visible to the model during `memory_recall` / `before_inference`.
