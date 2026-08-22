
# TopoSpace 1.2 beta2 — Agent Runtime Gateway

beta2 introduces a provider-neutral gateway/control plane above the 1.1 topological optimizer.

The intended integration is deliberately small:

    Existing agent / application
      -> OpenAI-compatible payload or TopoSpace SDK
      -> Agent Runtime Gateway
      -> context/memory/tool/skill/plan optimization
      -> logical model routing
      -> generation budget assignment
      -> downstream provider
      -> usage telemetry / A-B measurement

TopoSpace remains independent of LangChain. Framework adapters are compatibility surfaces, not architectural
dependencies.

The gateway currently provides a logical model route (fast/balanced/reasoning). Production deployments map
those logical classes to concrete provider/model identifiers through deployment configuration.

Important: generation-budget reduction is not itself token billing reduction. Commercial token/cost claims
must continue to use provider-reported actual usage from representative A/B workloads.
