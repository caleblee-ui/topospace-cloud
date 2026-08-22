
class CrossAgentTransfer:
    """Transfers a shared pattern into another agent as a local candidate, not a forced rule."""
    def import_for_agent(self,agent,items):
        imported=[]
        for item in items:
            agent.local_nodes[item.id]={
              "id":item.id,"kind":item.kind,"score":item.score,
              "source_agent":item.source_agent,"shared":True,
              "payload":dict(item.payload)
            }
            imported.append(item.id)
        return imported
