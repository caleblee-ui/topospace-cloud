
from unified_runtime.models import AgentState
from unified_runtime.router import UnifiedAdaptiveRouter
from coupled_geometry.coupling import CrossDomainCoupling
from coupled_geometry.adapter import GeometryCouplingAdapter
from coupled_geometry.models import JointTopologyState,DomainGeometryState

class CrossDomainGeometryRuntime:
    """
    Iteratively solves a coupled product space:
      X = X_memory × X_tool × X_skill × X_plan
    where each domain's local geometry is updated from other domains' selections.
    """
    DOMAINS=("memory","tool","skill","plan")

    def __init__(self,max_iterations=3,tolerance=.02):
        self.router=UnifiedAdaptiveRouter()
        self.coupling=CrossDomainCoupling()
        self.adapter=GeometryCouplingAdapter()
        self.max_iterations=max_iterations
        self.tolerance=tolerance

    def _make_state(self,base,domain,adapted):
        return AgentState(
          task_id=base.task_id,objective=base.objective,
          risk=adapted["risk"],ambiguity=adapted["ambiguity"],
          hierarchy=adapted["hierarchy"],candidate_pressure=adapted["candidate_pressure"],
          latency_pressure=adapted["latency_pressure"],metadata=dict(base.metadata)
        )

    def solve(self,base_state,spaces):
        routes={}
        signals={d:0.0 for d in self.DOMAINS}
        joint=JointTopologyState(base_state.task_id)

        for it in range(self.max_iterations):
            prev=dict(signals)
            new_routes={}
            for domain in self.DOMAINS:
                total=self.coupling.total_for(domain,signals)
                adapted=self.adapter.adapt_state(base_state,domain,total)
                state=self._make_state(base_state,domain,adapted)
                route=self.router.route(state,domain,spaces.get(domain,[]))

                # Coupling also modifies effective epsilon after policy selection.
                decision=route["decision"]
                coupled_epsilon=max(.08,min(1.0,decision.epsilon*(1+.35*total)))
                route["coupled_epsilon"]=coupled_epsilon

                # Re-filter selected neighborhood against coupled epsilon if geometry rows available.
                if route["selected"]:
                    route["selected"]=[
                      x for x in route["selected"]
                      if x.get("geometry",{}).get("distance",0)<coupled_epsilon
                    ]

                new_routes[domain]=route
                signals[domain]=self.adapter.selection_strength(route)

                joint.domains[domain]=DomainGeometryState(
                  domain=domain,
                  epsilon=coupled_epsilon,
                  p=decision.p,
                  aggregator=decision.aggregator,
                  selected_ids=[x["id"] for x in route["selected"]],
                  influence={"incoming":total,"strength":signals[domain]}
                )

            routes=new_routes
            joint.iteration=it+1
            delta=max(abs(signals[d]-prev[d]) for d in self.DOMAINS)
            if delta<self.tolerance:
                break

        return {"joint_state":joint,"routes":routes,"signals":signals}
