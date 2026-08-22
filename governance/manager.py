
from __future__ import annotations
from governance.signing import PolicySigner
from governance.approval import ApprovalWorkflow
from governance.lineage import PolicyLineage
from governance.scheduler import RolloutScheduler

class PolicyGovernanceManager:
    def __init__(self,signing_secret="change-me",required_approvals=1):
        self.signer=PolicySigner(signing_secret)
        self.approvals=ApprovalWorkflow(required_approvals)
        self.lineage=PolicyLineage()
        self.scheduler=RolloutScheduler()

    def submit(self,request_id,tenant_id,task_type,version,payload,requested_by,parent_hash=None):
        signed=self.signer.sign(tenant_id,task_type,version,payload)
        lineage=self.lineage.append(tenant_id,task_type,version,payload,parent_hash,requested_by,"submitted")
        approval=self.approvals.create(request_id,tenant_id,task_type,version,requested_by)
        return {"signed":signed,"lineage":lineage,"approval":approval}

    def approve_and_schedule(self,request_id,approver,when_ts,percent=100):
        r=self.approvals.approve(request_id,approver)
        if r.status!="approved":return {"approved":False,"request":r}
        item=self.scheduler.schedule(when_ts,r.tenant_id,r.task_type,r.version,percent)
        return {"approved":True,"request":r,"rollout":item}
