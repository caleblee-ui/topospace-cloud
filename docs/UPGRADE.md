
# Upgrade Procedure

1. Create a backup of persistent TopoSpace state.
2. Verify backup manifest checksums.
3. Deploy candidate version using canary/blue-green rollout.
4. Run registered migrations against a staging copy.
5. Validate `/healthz`, `/readyz`, optimization contract tests and customer smoke tests.
6. Promote traffic.
7. Retain the previous release and backup until the rollback window closes.
