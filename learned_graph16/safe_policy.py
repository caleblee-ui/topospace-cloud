
class SafeExecutionGraphPolicy:
    """
    Enforces path-level guardrails outside the learned utility.
    """
    def __init__(self,policy,forbid_fast_only_above_risk=.7,require_reasoning_above_risk=.9):
        self.policy=policy
        self.forbid_fast_only_above_risk=forbid_fast_only_above_risk
        self.require_reasoning_above_risk=require_reasoning_above_risk

    def route(self,ctx):
        out=self.policy.route(ctx)
        chosen=out["selected"]
        if ctx.risk>=self.require_reasoning_above_risk:
            for row in out["ranking"]:
                if "reasoning" in row["stages"]:
                    out["selected"]=row["path"];out["guardrail_override"]=True;return out
        if ctx.risk>=self.forbid_fast_only_above_risk and chosen=="fast_only":
            for row in out["ranking"]:
                if row["path"]!="fast_only":
                    out["selected"]=row["path"];out["guardrail_override"]=True;break
        return out
