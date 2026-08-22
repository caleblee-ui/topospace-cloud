# TopoSpace Cloud 1.3.0-alpha1
This layer turns TopoSpace 1.2 GA into a deployable multi-tenant middleware surface.

Implemented:
- `/v1/chat/completions` OpenAI-style request shape
- bearer API keys with hashed storage
- tenant plans and isolation boundary
- sliding-window rate limiting
- token/cost usage metering and quotas
- stable TopoSpace GA optimizer behind the HTTP surface
- provider-neutral execution-plan response

The provider adapter is intentionally separate. This avoids pretending that a real model call occurred when no external provider credentials are configured.
Next production work: persistent key/tenant store, real provider adapters, streaming/SSE, billing processor, distributed rate limiting and deployment manifests.
