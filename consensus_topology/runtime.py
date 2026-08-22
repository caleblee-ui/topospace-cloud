
from consensus_topology.consensus import TopologicalConsensus
from consensus_topology.negotiation import ConsensusNegotiator
class TopologicalMultiAgentConsensusRuntime:
    def __init__(self):
        self.consensus=TopologicalConsensus();self.negotiator=ConsensusNegotiator();self.history=[]
    def resolve(self,task_id,proposals):
        ranked=self.consensus.aggregate(proposals)
        decision=self.negotiator.decide(ranked)
        out={"task_id":task_id,"decision":decision,"ranking":ranked}
        self.history.append(out);return out
