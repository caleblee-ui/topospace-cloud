
class SafeRoutingPolicy:
    def __init__(self,policy,disallowed_high_risk=None):
        self.policy=policy;self.disallowed_high_risk=set(disallowed_high_risk or [])
    def route(self,ctx):
        out=self.policy.route(ctx)
        if ctx.risk>=.8 and out["selected"] in self.disallowed_high_risk:
            for r in out["ranking"]:
                if r["model"] not in self.disallowed_high_risk:
                    out["selected"]=r["model"];out["guardrail_override"]=True;break
        return out
