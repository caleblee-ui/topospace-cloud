
# Enterprise Policy Governance

v3.6 adds:
- signed policy artifacts
- human approval gates
- scheduled rollout
- multi-region policy replication
- disaster-recovery export/restore
- audit-grade lineage
- tenant/task learning isolation

The reference signing implementation uses HMAC for dependency-light validation. Enterprise deployments
should bind signing keys to KMS/HSM-backed key management and use the organization's approval identity system.
