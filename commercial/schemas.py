def validate_optimize_request(obj):
    errors=[]
    if not isinstance(obj,dict): return ["request_not_object"]
    if "objective" not in obj or not isinstance(obj.get("objective"),str): errors.append("objective_required")
    if "context" in obj and not isinstance(obj["context"],list): errors.append("context_must_be_list")
    if "agents" in obj and not isinstance(obj["agents"],list): errors.append("agents_must_be_list")
    for k in ("uncertainty","drift","complexity","cost_pressure"):
        if k in obj:
            try:
                v=float(obj[k])
                if not 0<=v<=1: errors.append(k+"_out_of_range")
            except Exception: errors.append(k+"_invalid")
    return errors
