
def marketing_claim(summary, min_success_delta_pp=-2.0, metric="input_tokens"):
    m=summary["metrics"][metric]
    success=summary["success"]
    lower=m["reduction_pct_ci95"][0]
    allowed=success["delta_pp_ci95"][0] >= min_success_delta_pp
    if allowed and lower>0:
        return {
          "eligible":True,
          "claim":f"Reduced {metric.replace('_',' ')} by at least {lower:.1f}% in this benchmark (95% bootstrap CI) while staying within the configured success-rate guardrail.",
          "lower_bound_pct":lower
        }
    return {"eligible":False,"claim":"Insufficient evidence for a marketing percentage claim from this benchmark.","lower_bound_pct":lower}
