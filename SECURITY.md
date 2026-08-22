# Security Policy

## Supported version

Security fixes are currently targeted at the latest `1.3.x` beta release.

## Reporting a vulnerability

Do not open a public issue for a suspected vulnerability. Use GitHub's private vulnerability reporting or private security-advisory workflow for this repository and include:

- affected component and version
- reproduction steps or proof of concept
- expected impact
- suggested mitigation, if available

Please allow maintainers time to investigate before public disclosure.

## Beta security boundaries

TopoSpace 1.3.0-beta1 includes reference implementations and adapter boundaries. In particular:

- the filesystem-copy patch sandbox is not a kernel, VM, or microVM boundary;
- local/in-memory stores are not billing-grade or multi-instance persistence;
- customer OIDC requires production JWKS signature verification;
- TLS termination, WAF, KMS/HSM, secret rotation, and deployment isolation belong to the production platform;
- upstream provider credentials must remain in a secret manager and must never be committed.

Run untrusted agent code in a hardened container, VM, or microVM. Use least-privilege provider keys, explicit tenant isolation, deployment monitoring, and durable external stores before customer traffic.
