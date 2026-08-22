
# TopoSpace Cloud — Replit Deployment Guide

**Target:** TopoSpace Cloud 1.3.0-beta1  
**Recommended Replit deployment:** Autoscale for an HTTP API. For workloads that must stay continuously warm, Reserved VM can be considered.

> **License notice:** The public source release is licensed under PolyForm Noncommercial 1.0.0. Public availability does not grant commercial-use rights. Any commercial deployment requires a separate written license from the licensor.

## 1. Upload the project

Create a Python Replit App and upload/extract the contents of the TopoSpace package so that the project root contains:

- `main.py`
- `.replit`
- `requirements.txt`
- `cloud19/`, `cloud20/`, `cloud21/`
- the TopoSpace runtime packages

Do not place the ZIP itself inside another nested project directory unless you update the run path.

## 2. Install dependencies

The only required serving dependency added for Replit is:

```bash
uvicorn>=0.30,<1
```

Replit should install `requirements.txt`. If needed, run:

```bash
pip install -r requirements.txt
```

## 3. Add Replit Secrets

Open **Secrets** in Replit and add at minimum:

```text
TOPOSPACE_API_KEY=<customer-facing-secret>
TOPOSPACE_TENANT_ID=default

PRIMARY_PROVIDER_BASE_URL=https://api.openai.com/v1
PRIMARY_PROVIDER_API_KEY=<provider-secret>
PRIMARY_PROVIDER_NAME=primary
```

Optional commercial controls:

```text
TOPOSPACE_RPM=60
TOPOSPACE_MONTHLY_TOKEN_LIMIT=1000000
TOPOSPACE_MONTHLY_COST_LIMIT=100
PROVIDER_RETRIES=1
```

Optional fallback provider:

```text
FALLBACK_PROVIDER_BASE_URL=<OpenAI-compatible base URL>
FALLBACK_PROVIDER_API_KEY=<fallback provider key>
FALLBACK_PROVIDER_NAME=fallback
```

Never commit actual API keys to `.env`, `.replit`, source code, GitHub, or the ZIP distributed to customers. `.env.example` is only a template.

## 4. Development test

Click **Run** or run:

```bash
uvicorn main:app --host 0.0.0.0 --port 3000
```

Health check:

```text
GET /healthz
```

Expected response:

```json
{"ok": true, "service": "topospace-cloud"}
```

## 5. API test

Send:

```bash
curl -X POST "$BASE_URL/v1/chat/completions"   -H "Authorization: Bearer $TOPOSPACE_API_KEY"   -H "Content-Type: application/json"   -d '{
    "model": "auto",
    "messages": [{"role":"user","content":"Explain this architecture."}],
    "max_tokens": 800,
    "topospace_state": {
      "risk": 0.2,
      "ambiguity": 0.4,
      "hierarchy": 0.5
    }
  }'
```

TopoSpace performs its Meta-Policy decision and then calls the configured provider adapter. The response is OpenAI-style and also includes a `topospace` block with optimization metadata.

## 6. Streaming

Set:

```json
"stream": true
```

The endpoint returns `text/event-stream` and terminates with:

```text
data: [DONE]
```

## 7. Publish on Replit

For this HTTP API, choose **Autoscale Deployment**. Configure the deployment to run:

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

The included `.replit` already defines a deployment run command using `${PORT:-3000}`.

After deployment, use the production `replit.app` URL or attach a custom domain. Do not use the temporary `replit.dev` development URL as a commercial endpoint.

## 8. Production checklist before customer traffic

- Set `ALLOW_MOCK_PROVIDER=false`.
- Store every production secret in Replit Secrets.
- Configure a primary provider and preferably a fallback provider.
- Test `/healthz`.
- Test normal and streaming requests.
- Test invalid API keys.
- Test rate-limit behavior.
- Confirm monthly token/cost limits.
- Confirm fallback by intentionally disabling the primary in staging.
- Turn on Replit App Monitoring for the published app.
- Use a custom production domain such as `api.example.com`.
- Keep a staging deployment separate from production.
- Export billing/usage records to persistent storage before relying on them for invoicing.

## 9. Important current limitation

The current beta has a SQLite/local persistence reference and Redis/PostgreSQL adapter boundaries, but Replit production billing and API-key state should ultimately use a persistent production datastore. Do not treat in-memory usage state as an accounting system of record.

The included OpenAI-compatible HTTP provider supports real non-streaming provider execution. Streaming currently uses the configured provider adapter's stream contract; provider-specific upstream streaming adapters should be hardened before high-volume commercial traffic.

## 10. Recommended rollout

Use three environments:

```text
Development → Staging → Production
```

Start with internal traffic, then a limited customer beta. Keep TopoSpace's champion/challenger and rollback logic enabled, but also use deployment-level rollback and health monitoring for infrastructure failures.
