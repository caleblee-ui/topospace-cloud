
class CollectiveCognitiveBridge:
    """Publishes semantic cognitive memories as shared knowledge candidates."""
    def publish_semantic(self,agent_id,cognitive_runtime,collective_runtime):
        patterns=[]
        for m in cognitive_runtime.layers.layers["semantic"].values():
            patterns.append({
              "id":f"semantic:{m.id}",
              "kind":"semantic_memory",
              "content":m.content,
              "tags":list(m.metadata.get("tags",[])),
              "success_rate":m.success_rate,
              "reward":max(m.utility,m.confidence),
              "access_scope":m.metadata.get("access_scope","tenant")
            })
        return collective_runtime.publish_success(agent_id,patterns,.65)
