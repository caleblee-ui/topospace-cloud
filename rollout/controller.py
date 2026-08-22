
from dataclasses import dataclass

@dataclass
class RolloutState:
    stable_version:str
    candidate_version:str|None=None
    candidate_percent:int=0

class RolloutController:
    def __init__(self,stable_version):
        self.state=RolloutState(stable_version)

    def start_canary(self,candidate_version,percent=5):
        self.state.candidate_version=candidate_version
        self.state.candidate_percent=max(0,min(100,int(percent)))
        return self.state

    def promote(self):
        if self.state.candidate_version:
            self.state.stable_version=self.state.candidate_version
            self.state.candidate_version=None
            self.state.candidate_percent=0
        return self.state

    def rollback(self):
        self.state.candidate_version=None
        self.state.candidate_percent=0
        return self.state

    def route(self,key):
        if not self.state.candidate_version or self.state.candidate_percent<=0:return self.state.stable_version
        bucket=abs(hash(key))%100
        return self.state.candidate_version if bucket<self.state.candidate_percent else self.state.stable_version
