
# Enterprise Trust Layer

v3.7 adds:
- signed service identities for zero-trust service-to-service authorization
- mTLS configuration contract
- policy attestation
- lightweight CycloneDX-like SBOM generation
- signed release artifacts
- runtime source integrity verification
- compliance export bundles

Reference signing uses HMAC to remain dependency-light. Production deployments should use asymmetric
KMS/HSM-backed keys, real certificate validation and established supply-chain standards such as
Sigstore/cosign and official CycloneDX/SPDX generators.
