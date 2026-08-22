
class ExecutionGraphCostModel:
    def estimate(self,graph,profiles):
        by={p.name:p for p in profiles}
        cost=0.0;lat=0.0
        for n in graph.nodes:
            if n.kind=="model" and n.model in by:
                p=by[n.model]
                cost+=p.input_cost_per_1k+p.output_cost_per_1k
                lat+=p.latency_ms
            elif n.kind=="tool":
                lat+=150
            elif n.kind=="memory":
                lat+=25
        return {"nominal_cost":cost,"nominal_latency_ms":lat}
