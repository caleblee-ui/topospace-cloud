
TOOLS=[
 {"name":"topospace_memory_recall","description":"Recall the smallest topologically relevant set of TorusDB agent memories for the current task.",
  "inputSchema":{"type":"object","properties":{"query":{"type":"string"},"limit":{"type":"integer","minimum":1,"maximum":100},"max_return":{"type":"integer","minimum":1,"maximum":30}},"required":["query"]}},
 {"name":"topospace_memory_get","description":"Get one TorusDB agent memory by id.",
  "inputSchema":{"type":"object","properties":{"memory_id":{"type":"string"}},"required":["memory_id"]}},
 {"name":"topospace_memory_remember","description":"Store or update an agent memory in TorusDB.",
  "inputSchema":{"type":"object","properties":{"id":{"type":"string"},"content":{"type":"string"},"ciphertext":{"type":"string"},"metadata":{"type":"object"},"tokens":{"type":"integer"}},"required":["id"]}},
 {"name":"topospace_memory_forget","description":"Delete an agent memory by id.",
  "inputSchema":{"type":"object","properties":{"memory_id":{"type":"string"}},"required":["memory_id"]}}
]
