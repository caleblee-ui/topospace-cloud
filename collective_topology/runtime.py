
from collective_topology.models import AgentTopologyState
from collective_topology.shared_space import SharedTopologySpace
from collective_topology.broker import CollectiveKnowledgeBroker
from collective_topology.federation import TopologyFederation
from collective_topology.transfer import CrossAgentTransfer

class CollectiveTopologyRuntime:
    def __init__(self):
        self.agents={}
        self.shared=SharedTopologySpace()
        self.broker=CollectiveKnowledgeBroker()
        self.federation=TopologyFederation()
        self.transfer=CrossAgentTransfer()

    def register_agent(self,agent_id,tenant_id="default",specialization=None):
        a=AgentTopologyState(agent_id,tenant_id,set(specialization or []))
        self.agents[agent_id]=a
        return a

    def publish_success(self,agent_id,patterns,min_reward=.75):
        return self.federation.promote_patterns(self.agents[agent_id],self.shared,patterns,min_reward)

    def sync_agent(self,agent_id,limit=12):
        a=self.agents[agent_id]
        selected=self.broker.select(a,self.shared,limit)
        imported=self.transfer.import_for_agent(a,selected)
        return {"selected":[x.id for x in selected],"imported":imported}

    def snapshot(self):
        return {
          "agents":{k:{"tenant_id":v.tenant_id,"specialization":sorted(v.specialization),"local_nodes":len(v.local_nodes)} for k,v in self.agents.items()},
          "shared_items":len(self.shared.items),
          "shared_links":len(self.shared.links)
        }
