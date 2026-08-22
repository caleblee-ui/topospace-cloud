
# Production Deployment

Run:
```bash
python server/app.py
```

Optional API key auth:
- `TOPOSPACE_API_KEY_ID`
- `TOPOSPACE_API_KEY_SECRET`

The production server exposes:
- `GET /health`
- `POST /v1/optimize`

Use a reverse proxy/load balancer with TLS in production. SQLite-backed stores are reference defaults;
replace with managed durable storage for multi-node deployments.
