---
name: topospace-memory
description: Recall, store, update, or forget long-term AI agent memory using TorusDB with TopoSpace topological context selection. Use when a task needs relevant prior decisions, project history, durable agent memory, or memory cleanup.
---

Use this skill when the user or agent needs durable memory beyond the current conversation.

1. For recall, call `topospace_memory_recall` before requesting many raw memories.
2. Pass the concrete task or question as `query`. Prefer the returned topologically selected memories rather than asking for the full memory corpus.
3. If the user asks for one known memory by identifier, call `topospace_memory_get`.
4. When a durable fact, decision, result, or reusable agent state should be stored, call `topospace_memory_remember`.
5. When the user explicitly asks to delete durable memory, call `topospace_memory_forget`.
6. Treat `ciphertext` as opaque protected content. Do not claim to decrypt it unless another authorized tool explicitly provides that capability.
7. Do not invent missing memory contents. If recall returns no relevant memories, continue without pretending prior knowledge exists.
8. Prefer concise memory results to reduce context tokens. Only broaden recall when uncertainty remains high or the current attempt failed.

When presenting recalled memories, distinguish stored facts from new inferences.
