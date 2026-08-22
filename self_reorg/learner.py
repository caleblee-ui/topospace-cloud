
class TopologyReinforcementLearner:
    """Updates node/edge strengths from execution feedback."""
    def __init__(self,node_lr=.18,edge_lr=.22,decay=.01):
        self.node_lr=node_lr;self.edge_lr=edge_lr;self.decay=decay

    def update_node(self,node,reward,success=True):
        target=max(0.0,min(1.0,float(reward) if success else 0.0))
        node.score=max(0.0,min(1.0,(1-self.node_lr)*node.score+self.node_lr*target))
        return node.score

    def update_edge(self,edge,reward,success=True):
        target=max(0.0,min(1.0,float(reward) if success else 0.0))
        edge.weight=max(0.0,min(1.0,(1-self.edge_lr)*edge.weight+self.edge_lr*target))
        return edge.weight

    def decay_graph(self,graph):
        for node in graph.nodes.values():
            node.score=max(0.0,node.score*(1-self.decay))
        for edge in graph.edges:
            edge.weight=max(0.0,edge.weight*(1-self.decay))
