
# TopoSpace Customer Deployment Edition v3.1

Deployment building blocks:
- Helm chart for Kubernetes
- Terraform composition scaffold
- OIDC identity abstraction
- tenant usage metering
- signed commercial license tokens
- backup/restore manager
- schema/config migration runner
- admin tenant operations

Production requirements still supplied by the customer/cloud environment:
- TLS ingress/WAF
- issuer JWKS signature verification for OIDC
- managed PostgreSQL/Redis
- external KMS/secrets manager
- log/SIEM export
- billing provider if SaaS monetization is required
