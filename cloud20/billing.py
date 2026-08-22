
from collections import defaultdict
class BillingLedger:
    def __init__(self):self.entries=[];self.balance=defaultdict(float)
    def record(self,tenant_id,request_id,provider,model,cost,input_tokens,output_tokens):
        row={"tenant_id":tenant_id,"request_id":request_id,"provider":provider,"model":model,
             "cost":float(cost),"input_tokens":int(input_tokens),"output_tokens":int(output_tokens)}
        self.entries.append(row);self.balance[tenant_id]+=row["cost"];return row
    def invoice_summary(self,tenant_id):
        rows=[x for x in self.entries if x["tenant_id"]==tenant_id]
        return {"tenant_id":tenant_id,"requests":len(rows),"provider_cost":sum(x["cost"] for x in rows),
                "tokens":sum(x["input_tokens"]+x["output_tokens"] for x in rows)}
