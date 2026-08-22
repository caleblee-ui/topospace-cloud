
from collections import defaultdict
class UsageMeter:
    def __init__(self):self.rows=[];self.totals=defaultdict(lambda:{"requests":0,"input_tokens":0,"output_tokens":0,"cost":0.0})
    def record(self,tenant_id,model,input_tokens,output_tokens,cost,latency_ms,success):
        r={"tenant_id":tenant_id,"model":model,"input_tokens":int(input_tokens),"output_tokens":int(output_tokens),
           "cost":float(cost),"latency_ms":float(latency_ms),"success":bool(success)}
        self.rows.append(r);t=self.totals[tenant_id];t["requests"]+=1;t["input_tokens"]+=r["input_tokens"];t["output_tokens"]+=r["output_tokens"];t["cost"]+=r["cost"];return r
    def quota_ok(self,plan):
        t=self.totals[plan.tenant_id]
        return t["input_tokens"]+t["output_tokens"]<=plan.monthly_token_limit and t["cost"]<=plan.monthly_cost_limit
