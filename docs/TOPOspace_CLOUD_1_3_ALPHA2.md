# TopoSpace Cloud 1.3.0-alpha2
alpha2 adds the production gateway execution layer:

- provider adapter contract and executable chat completions
- provider retry/fallback with circuit breaker
- streaming event/SSE primitives
- usage metering after real provider responses
- billing ledger
- SQLite tenant/API-key reference persistence with PostgreSQL adapter boundary
- distributed rate-limit adapter boundary for Redis

The bundled DeterministicProvider is a test provider only. No claim is made that external commercial providers
were invoked in validation. Production deployments should configure concrete provider adapters and credentials.
