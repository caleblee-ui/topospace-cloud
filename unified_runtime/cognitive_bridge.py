
from general_geometry.views import ViewValue

class RuntimeSpaceBuilder:
    VIEW_NAMES=("semantic","structural","history","policy","security","cost","reliability")

    def build_candidate(self,obj):
        vals=obj.get("views")
        if vals is None:
            vals=[
              obj.get("semantic_distance",.5),
              obj.get("structural_distance",.5),
              obj.get("history_distance",.5),
              obj.get("policy_distance",0),
              obj.get("security_distance",0),
              obj.get("cost_distance",.3),
              obj.get("reliability_distance",.3),
            ]
        return {
          "id":obj["id"],
          "kind":obj.get("kind","memory"),
          "views":[ViewValue(n,float(v)) for n,v in zip(self.VIEW_NAMES,vals)],
          "payload":obj
        }

    def build_space(self,items):
        return [self.build_candidate(x) for x in items]
