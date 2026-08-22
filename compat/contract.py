
REQUIRED_RESPONSE_KEYS={"api_version","engine_version","request_id","tenant_id","project_id","result","latency_ms"}
REQUIRED_RESULT_KEYS={"context","team","context_tokens"}

class ContractCompatibility:
    def validate_response(self,obj):
        errors=[]
        missing=REQUIRED_RESPONSE_KEYS-set(obj)
        if missing: errors.append("missing_response_keys:"+",".join(sorted(missing)))
        result=obj.get("result",{})
        rmissing=REQUIRED_RESULT_KEYS-set(result)
        if rmissing: errors.append("missing_result_keys:"+",".join(sorted(rmissing)))
        if obj.get("api_version")!="v1": errors.append("api_version_changed")
        return {"ok":not errors,"errors":errors}

    def compare_request_schema(self,old,new):
        old_req=set(old.get("required",[]));new_req=set(new.get("required",[]))
        added=sorted(new_req-old_req)
        return {"compatible":not added,"new_required_fields":added}
