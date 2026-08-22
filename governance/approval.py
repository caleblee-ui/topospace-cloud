
from __future__ import annotations
from dataclasses import dataclass,field
from time import time

@dataclass
class ApprovalRequest:
    id:str
    tenant_id:str
    task_type:str
    version:int
    requested_by:str
    status:str="pending"
    approvers:list=field(default_factory=list)
    created_at:float=field(default_factory=time)
    decided_at:float|None=None

class ApprovalWorkflow:
    def __init__(self,required_approvals=1):
        self.required_approvals=required_approvals
        self.requests={}

    def create(self,request_id,tenant_id,task_type,version,requested_by):
        r=ApprovalRequest(request_id,tenant_id,task_type,int(version),requested_by)
        self.requests[request_id]=r
        return r

    def approve(self,request_id,principal):
        r=self.requests[request_id]
        if principal not in r.approvers:r.approvers.append(principal)
        if len(r.approvers)>=self.required_approvals:
            r.status="approved";r.decided_at=time()
        return r

    def reject(self,request_id,principal):
        r=self.requests[request_id]
        r.status="rejected";r.approvers.append(principal);r.decided_at=time()
        return r
