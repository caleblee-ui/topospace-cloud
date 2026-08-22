
from __future__ import annotations
import json,time

class ComplianceExporter:
    def export(self,*,tenant_id,policies,audit_events,approvals,lineage,integrity,metadata=None):
        return {
          "schema":"topospace-compliance-v1",
          "generated_at":time.time(),
          "tenant_id":tenant_id,
          "policies":policies,
          "audit_events":audit_events,
          "approvals":approvals,
          "policy_lineage":lineage,
          "runtime_integrity":integrity,
          "metadata":metadata or {}
        }

    def to_json(self,bundle):
        return json.dumps(bundle,sort_keys=True,indent=2)
