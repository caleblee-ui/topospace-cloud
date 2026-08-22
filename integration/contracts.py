
INTEGRATION_MODES = {
  "embedded_python": {
    "description":"Import TopoSpaceMiddleware directly into a Python agent loop.",
    "protocol":"in-process"
  },
  "http_middleware": {
    "description":"Call TopoSpace production service before inference/tool execution.",
    "protocol":"REST"
  },
  "mcp": {
    "description":"Expose context, memory and state tools to MCP-capable clients.",
    "protocol":"MCP"
  },
  "sdk": {
    "description":"Use Python or TypeScript SDK from a custom agent runtime.",
    "protocol":"HTTP SDK"
  }
}
