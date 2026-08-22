
# TorusDB Agent Memory + TopoSpace + ChatGPT

Architecture:
`ChatGPT/Codex -> Skill -> MCP tool -> TopoSpace recall bridge -> TorusDB Agent Memory`

- TorusDB owns durable memory, encrypted/opaque payloads, storage and database policy.
- TopoSpace owns recall selection, topology, drift, persistence, token budgeting and quality expansion.
- The Skill teaches the workflow.
- The MCP server exposes live memory tools.

For ChatGPT development testing, deploy the MCP endpoint at stable HTTPS `/mcp` (or use the official
Secure MCP Tunnel), enable developer mode, add the MCP connection, inspect discovered tools, and test
the plugin skill. Before public deployment, validate the server with MCP Inspector and the current
official MCP SDK.
