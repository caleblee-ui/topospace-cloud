
# TopoSpace 1.2 beta1 — Provider-Neutral Agent Optimization Middleware

TopoSpace 1.2 moves from candidate-space benchmarks toward measurable LLM/agent execution.

## Positioning

TopoSpace is not a LangChain plugin and does not require LangChain. It is provider-neutral middleware placed
between an agent runtime and model/tool providers. Optional adapters can expose the same optimizer to LangChain
or other frameworks.

## New execution boundary

Agent / application
  -> TopoSpace middleware
  -> optimized Memory / Tool / Skill / Plan spaces
  -> provider adapter
  -> LLM / tool execution
  -> actual usage telemetry
  -> A/B experiment store
  -> joint geometry feedback

The A/B layer records provider-reported input/output tokens, tool calls, latency and external quality scores.
Only live representative workload results should be promoted to commercial savings claims.
