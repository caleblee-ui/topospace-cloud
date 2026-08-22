# TopoSpace Cloud 1.3.0-beta1 Limitations

This document separates implemented beta capabilities from production work.

## Implemented in the beta

- OpenAI-compatible `POST /v1/chat/completions`
- `GET /healthz`
- bearer API-key gate
- logical model routing
- primary/fallback provider primitives
- normal response and SSE streaming contracts
- tenant plan, rate-limit, quota, metering, and billing primitives
- Meta-Policy and PolicyOps primitives including shadow, promotion, rollout, and rollback
- Replit-ready ASGI entry point and deployment assets

## Not production-complete

- managed PostgreSQL/Redis persistence across instances
- billing-grade durable ledger and reconciliation
- full API-key issuance, rotation, revocation, and audit lifecycle
- customer IAM and verified OIDC/JWKS integration
- provider-specific upstream streaming hardening
- complete tenant/policy/usage operations console
- production TLS/WAF/KMS and deployment isolation controls

## Claim discipline

The included tests and deterministic benchmarks are engineering evidence. Public token-savings, cost-savings, latency, quality, or superiority claims require reproducible real-provider runs with pinned versions, frozen tasks, and external evaluation.
