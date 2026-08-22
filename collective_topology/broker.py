
class CollectiveKnowledgeBroker:
    """Scores shared knowledge for one agent without erasing its specialization."""
    def score(self,agent,item):
        payload=item.payload
        affinity=0.0
        tags=set(payload.get("tags",[]))
        if agent.specialization:
            affinity=len(tags & agent.specialization)/max(1,len(agent.specialization))
        source_bonus=.05 if item.source_agent==agent.agent_id else 0
        global_penalty=.03 if item.access_scope=="global" else 0
        return .55*item.score+.30*affinity+.10*float(payload.get("success_rate",.5))+source_bonus-global_penalty

    def select(self,agent,shared_space,limit=12):
        visible=shared_space.visible(agent.tenant_id,agent.agent_id)
        ranked=sorted(visible,key=lambda x:self.score(agent,x),reverse=True)
        return ranked[:limit]
