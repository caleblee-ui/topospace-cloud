
class CoupledExecutionComposer:
    """Produces one coherent execution bundle from the converged joint topology."""
    ORDER=("memory","skill","tool","plan")

    def compose(self,solution,max_per_domain=5):
        bundle=[]
        for d in self.ORDER:
            route=solution["routes"][d]
            for x in route.get("selected",[])[:max_per_domain]:
                bundle.append({"domain":d,"id":x["id"],"payload":x.get("payload",{})})
        return {
          "execution_bundle":bundle,
          "joint_iterations":solution["joint_state"].iteration,
          "domain_geometry":{
             d:{
               "aggregator":s.aggregator,
               "epsilon":s.epsilon,
               "p":s.p,
               "selected":len(s.selected_ids),
               "incoming_influence":s.influence.get("incoming",0)
             } for d,s in solution["joint_state"].domains.items()
          }
        }
