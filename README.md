# TopoSpace Cloud

**Version 1.3.0-beta1** · **PolyForm Noncommercial 1.0.0** · **Python 3.10+**

TopoSpace is a provider-neutral **AI Execution Optimization Plane**. It is not an AI model. It coordinates context selection, model routing, execution paths, and token budgets before and around model execution.

- Product page: [J1729Labs / TopoSpace](https://j1729labs.site/topospace)
- Source repository: [caleblee-ui/topospace-cloud](https://github.com/caleblee-ui/topospace-cloud)
- HTTP gateway: `POST /v1/chat/completions`
- Health check: `GET /healthz`
- License: [PolyForm Noncommercial 1.0.0](LICENSE)

> License notice: the source is publicly available for permitted noncommercial purposes. Commercial use requires a separate written license from the licensor. Because commercial use is restricted, this is a source-available release rather than an OSI-approved open-source license.
>
> Beta notice: this release is engineering software for evaluation and controlled pilots. It does not claim a verified token-savings percentage, cost-savings percentage, or performance advantage.

## Whitepaper

[**TopoSpace: Adaptive Topological State-Space Infrastructure for AI Agents**](docs/TopoSpace_Whitepaper_v2.0.pdf)  
Technical Whitepaper — Version 2.0, with a controlled simulation study · 66 pages · August 22, 2026.

## What TopoSpace coordinates

### Adaptive Geometry
Builds a task-conditioned neighborhood over memory, tools, skills, agents, code, and other execution objects.

### Model Routing
Chooses a logical provider path from workload complexity, coupling, expected usage, cost, latency, quality signals, and historical outcomes.

### Execution Graph
Compiles progressive Memory, Tool, and Model paths with confidence-driven escalation, early stopping, and path-level guardrails.

### Meta-Policy
Coordinates geometry, model routing, and execution-graph policy under one feedback objective while preserving deterministic safety overrides.

## PolicyOps

TopoSpace includes policy lifecycle primitives for controlled optimization:

1. **Shadow** — evaluate a candidate without changing live decisions.
2. **Champion / challenger** — compare accepted and candidate policies.
3. **Promotion** — advance only when configured quality and safety gates pass.
4. **Rollback** — return to the last accepted policy when guardrails are crossed.

## Quick start

```bash
python -m pip install -r requirements.txt
cp .env.example .env
# Replace placeholders locally. Never commit .env.
uvicorn main:app --host 0.0.0.0 --port 3000
```

Check the service:

```bash
curl http://127.0.0.1:3000/healthz
```

Expected response:

```json
{"ok": true, "service": "topospace-cloud"}
```

## OpenAI-compatible gateway

```bash
curl -X POST "http://127.0.0.1:3000/v1/chat/completions" \
  -H "Authorization: Bearer $TOPOSPACE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "auto",
    "messages": [
      {"role": "user", "content": "Explain this architecture."}
    ],
    "max_tokens": 800,
    "stream": false,
    "topospace_state": {
      "risk": 0.2,
      "ambiguity": 0.4,
      "hierarchy": 0.5
    }
  }'
```

The gateway returns an OpenAI-style response plus TopoSpace optimization metadata. Set `"stream": true` for the current SSE contract, which terminates with `data: [DONE]`.

## Provider configuration

Set production values through your deployment platform's secret manager. Do not commit them.

```text
TOPOSPACE_API_KEY=<customer-facing-secret>
TOPOSPACE_TENANT_ID=default
PRIMARY_PROVIDER_BASE_URL=https://api.openai.com/v1
PRIMARY_PROVIDER_API_KEY=<provider-secret>
PRIMARY_PROVIDER_NAME=primary
ALLOW_MOCK_PROVIDER=false
```

A fallback OpenAI-compatible provider can be configured with the `FALLBACK_PROVIDER_*` variables documented in [.env.example](.env.example).

## Validation

The supplied 1.3.0-beta1 release record reports:

- 293 regression tests passed
- `compileall` passed
- `main.py` byte-compilation passed
- Replit deployment assets passed

See [VALIDATION.md](VALIDATION.md). These are local engineering checks, not external provider or customer production benchmarks.

## Current beta limitations

- PostgreSQL and Redis are adapter boundaries, not complete managed production backends.
- In-memory/local usage and billing primitives are not an accounting system of record.
- Durable API-key lifecycle, customer IAM, and OIDC verification require production work.
- Provider-specific upstream streaming needs additional high-volume hardening.
- A complete operations console and managed policy administration are roadmap work.
- Real-provider behavior depends on the configured provider and deployment environment.

See [docs/BETA_LIMITATIONS.md](docs/BETA_LIMITATIONS.md) and [ARCHITECTURE.md](ARCHITECTURE.md).

## Repository map

```text
main.py                 ASGI application entry point
cloud19/                tenant, key, quota, and OpenAI compatibility primitives
cloud20/                provider execution, resilient routing, billing primitives
cloud21/                Replit-ready ASGI gateway and bootstrap
meta_policy17/          coordinated policy control
model_router13/         topology-aware model routing
execution_graph15/      execution graph construction
policyops/              shadow, promotion, rollout, and rollback primitives
runtime*/               runtime and SDK layers
tests/                  regression suite
docs/                   architecture, deployment, and release documentation
```

The repository also contains earlier research/runtime modules retained for compatibility and regression coverage. Component-specific historical version markers do not replace the Cloud release version stated here.

## Development

```bash
python -m pytest -q
python -m compileall .
python -m py_compile main.py
```

Contributions should preserve provider neutrality and distinguish deterministic fixtures from public performance evidence. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Deployment

For Replit deployment, follow [docs/REPLIT_COMMERCIAL_DEPLOYMENT.md](docs/REPLIT_COMMERCIAL_DEPLOYMENT.md). Before customer traffic, disable the mock provider, configure secrets, test authentication and quotas, validate fallback behavior, and use durable external storage for billing-grade records.

## Security

This beta includes reference implementations and adapter boundaries that are not complete security boundaries. Review [SECURITY.md](SECURITY.md) before deployment and report vulnerabilities privately.

## License

Copyright 2026 TopoSpace contributors. The source is publicly available under the [PolyForm Noncommercial License 1.0.0](LICENSE). Commercial use is not permitted by the public license and requires a separate written license from the licensor.
