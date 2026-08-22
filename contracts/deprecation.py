
from dataclasses import dataclass

@dataclass
class DeprecationPolicy:
    api_major:str="v1"
    minimum_notice_days:int=180
    breaking_changes_require_new_major:bool=True

    def validate_change(self,breaking,notice_days,new_api_major=None):
        errors=[]
        if breaking and self.breaking_changes_require_new_major and new_api_major==self.api_major:
            errors.append("breaking_change_requires_new_api_major")
        if breaking and notice_days<self.minimum_notice_days:
            errors.append("insufficient_deprecation_notice")
        return {"ok":not errors,"errors":errors}
