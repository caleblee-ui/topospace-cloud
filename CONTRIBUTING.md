# Contributing to TopoSpace

## Principles

- Keep the optimization plane provider-neutral.
- Preserve deterministic safety and policy override paths.
- Distinguish synthetic fixtures and regression evidence from external performance claims.
- Do not commit credentials, customer data, local databases, or generated build artifacts.
- Contributions are distributed under the repository's PolyForm Noncommercial 1.0.0 license unless maintainers agree otherwise in writing.
- Keep changes focused and include tests for behavioral changes.

## Local checks

```bash
python -m pytest -q
python -m compileall .
python -m py_compile main.py
```

For gateway changes, also verify:

- `GET /healthz`
- valid and invalid bearer API keys
- normal and streaming chat requests
- rate-limit and quota behavior
- primary-provider failure and fallback behavior

## Pull requests

Explain the product behavior being changed, the validation performed, and any production boundary that remains. New optimization claims must include a reproducible benchmark manifest, pinned provider/model versions, frozen tasks, and an external evaluation method.
