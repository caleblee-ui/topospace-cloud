
class AdaptiveExecutionPlanner:
    def compose(self,routes,max_items_per_domain=6):
        bundle={}
        for domain,result in routes.items():
            bundle[domain]=result["selected"][:max_items_per_domain]
        return {
          "bundle":bundle,
          "geometry":{
             d:{
               "aggregator":r["decision"].aggregator,
               "epsilon":r["decision"].epsilon,
               "p":r["decision"].p,
               "confidence":r["decision"].confidence,
               "blocked_by_constraints":len(r.get("blocked_by_constraints",[]))
             } for d,r in routes.items()
          }
        }
