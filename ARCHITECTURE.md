# TopoSpace Cloud 1.3.0-beta1 Architecture

## Product boundary

TopoSpace is a provider-neutral AI Execution Optimization Plane. It does not train or replace an AI model. It sits between an agent/application and one or more model providers to coordinate context, routing, execution, and budgets.

```text
Agent / application
        |
OpenAI-compatible gateway
        |
Meta-Policy control plane
  |          |           |
Geometry   Routing   Execution graph
  |          |           |
Context   Provider    Progressive path
        \     |     /
      Guarded execution
             |
 Primary provider -> fallback provider
             |
 Usage, outcome, and policy feedback
```

## Cloud gateway

`main.py` exports the ASGI application built by `cloud21.bootstrap.build_service()` and `cloud21.asgi.ProductionASGI`.

Current public routes:

- `GET /`
- `GET /health`
- `GET /healthz`
- `POST /v1/chat/completions`

The chat route accepts an OpenAI-style request, requires the configured bearer API key, and can return a normal JSON response or the current SSE stream contract.

## Control layers

### 1. Adaptive Geometry

The geometry layer constructs task-conditioned neighborhoods over execution objects. The broader research runtime includes adaptive exponents, component weights, epsilon selection, bounded candidate sets, and contribution traces.

### 2. Model Routing

The routing layer evaluates logical model candidates using workload and topology signals together with expected usage, latency, cost, quality, and outcome history. Deterministic safety overrides remain available.

### 3. Execution Graph

The execution layer creates progressive Memory, Tool, and Model paths. Confidence-driven escalation and early stopping can avoid forcing every request through the same path.

### 4. Meta-Policy

The Meta-Policy coordinates geometry, routing, and graph policy under one feedback objective. PolicyOps provides shadow evaluation, champion/challenger comparison, gated promotion, staged rollout, and rollback primitives.

## Provider and reliability boundary

`cloud20` and `cloud21` assemble provider execution, retry/fallback, rate limits, tenant plans, metering, and billing primitives. The included OpenAI-compatible HTTP provider supports real non-streaming calls. Streaming uses the provider adapter contract and still needs provider-specific hardening before high-volume production use.

## Persistence boundary

The beta includes local/SQLite reference persistence and Redis/PostgreSQL adapter boundaries. Managed multi-instance persistence, billing-grade durability, and full API-key lifecycle management are not complete.

## Observability and feedback

Responses can include TopoSpace decision metadata, while runtime modules expose traces, usage, outcomes, and policy feedback. These primitives support evaluation and controlled learning; they do not by themselves establish a production monitoring or accounting system.

## Validation boundary

The release record reports 293 passing regression tests, compilation checks, and Replit deployment-asset checks. It does not establish external provider performance, customer production reliability, or a general token/cost reduction percentage.
