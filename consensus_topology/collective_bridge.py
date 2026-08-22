
from consensus_topology.proposal import TopologyProposal
class CollectiveConsensusBridge:
    """Builds proposals from agent-local candidates selected from collective topology."""
    def proposals_from_agents(self,collective_runtime,task_id,candidate_id,kind="pattern"):
        out=[]
        for aid,a in collective_runtime.agents.items():
            x=a.local_nodes.get(candidate_id)
            if not x:continue
            p=x.get("payload",{})
            out.append(TopologyProposal(
              agent_id=aid,task_id=task_id,candidate_id=candidate_id,kind=kind,
              confidence=float(p.get("confidence",x.get("score",.5))),
              utility=float(p.get("utility",x.get("score",.5))),
              distance=float(p.get("distance",.2)),
              evidence=float(p.get("success_rate",.5)),
              tags=set(p.get("tags",[]))
            ))
        return out
