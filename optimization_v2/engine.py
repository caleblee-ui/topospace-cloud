
from optimization_v2.hierarchy import HierarchicalTopology,TopologyNode
from optimization_v2.coarse_to_fine import CoarseToFineRecall
from optimization_v2.consolidation import AdaptiveMemoryConsolidator

class OptimizationEngineV2:
    def __init__(self):
        self.topology=HierarchicalTopology()
        self.recall=CoarseToFineRecall()
        self.consolidator=AdaptiveMemoryConsolidator()

    def optimize(self,items,token_budget=4000):
        nodes=[TopologyNode(
          id=str(x.get("id")),distance=float(x.get("distance",1)),
          utility=float(x.get("utility",x.get("importance",.5))),
          tokens=int(x.get("tokens",0)),payload=x
        ) for x in items]
        hierarchy=self.topology.organize(nodes)
        result=self.recall.select(hierarchy,token_budget=token_budget)
        selected=[n.payload for n in result["nodes"]]
        return {
          "context":selected,
          "context_tokens":result["tokens"],
          "visited_levels":result["visited_levels"],
          "input_tokens":sum(n.tokens for n in nodes),
          "token_reduction":1-(result["tokens"]/max(1,sum(n.tokens for n in nodes)))
        }

    def consolidate_memory(self,records):
        return self.consolidator.consolidate(records)
