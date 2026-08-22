
from dataclasses import dataclass,field
@dataclass
class TopologyProposal:
    agent_id:str
    task_id:str
    candidate_id:str
    kind:str
    confidence:float
    utility:float
    distance:float
    evidence:float=.5
    tags:set=field(default_factory=set)
