
# Optimization Engine v2

TopoSpace 1.1 introduces a topology-first optimization path:
1. place context/memory/tool candidates into epsilon shells,
2. search coarse-to-fine from the nearest shell outward,
3. rank within shells using semantic relevance + topological proximity + utility - drift,
4. stop widening when the quality/budget condition is met,
5. consolidate near-duplicate durable memories into compact representatives.

This architecture is intended for agent context assembly, memory recall, tool selection and multi-agent routing.
Token savings from synthetic benchmarks are engineering evidence only; external marketing claims should be based
on representative production workloads and should report task success alongside token reduction.
