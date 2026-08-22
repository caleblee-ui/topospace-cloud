
class TopologyFederation:
    """Aggregates successful local patterns into a shared topology representation."""
    def promote_patterns(self,agent,shared_space,patterns,min_reward=.75):
        published=[]
        for p in patterns:
            reward=float(p.get("reward",0))
            if reward<min_reward:continue
            ident=p.get("id") or f'{agent.agent_id}:{p.get("kind","pattern")}:{len(shared_space.items)}'
            from collective_topology.models import SharedKnowledge
            item=SharedKnowledge(
                id=ident,kind=p.get("kind","pattern"),payload=dict(p),
                score=min(1.0,reward),source_agent=agent.agent_id,
                tenant_id=agent.tenant_id,access_scope=p.get("access_scope","tenant")
            )
            shared_space.publish(item);published.append(ident)
        return published
