
from model_router13.models import RoutingContext

class RoutingContextBuilder:
    def from_gateway(self,req,decision):
        geometry=decision.diagnostics.get("geometry",{}) if hasattr(decision,"diagnostics") else {}
        eps=[];couplings=[]
        for _,g in geometry.items():
            if isinstance(g,dict):
                if g.get("epsilon") is not None:eps.append(float(g["epsilon"]))
                if g.get("incoming_influence") is not None:couplings.append(abs(float(g["incoming_influence"])))
        topology_complexity=min(1.0,(sum(eps)/max(1,len(eps))) if eps else float(req.state.get("hierarchy",0)))
        coupling_strength=min(1.0,(sum(couplings)/max(1,len(couplings))) if couplings else float(req.state.get("coupling_strength",0)))
        return RoutingContext(
          risk=float(req.state.get("risk",0)),
          ambiguity=float(req.state.get("ambiguity",0)),
          topology_complexity=topology_complexity,
          coupling_strength=coupling_strength,
          candidate_pressure=float(req.state.get("candidate_pressure",0)),
          latency_pressure=float(req.state.get("latency_pressure",0)),
          expected_input_tokens=int(req.state.get("expected_input_tokens",decision.token_budget)),
          expected_output_tokens=int(req.state.get("expected_output_tokens",512)),
          expected_tool_calls=len(decision.selected_tools)
        )
