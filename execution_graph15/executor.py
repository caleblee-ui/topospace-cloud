
class GraphExecutionController:
    """
    Decides which graph edges are activated from runtime feedback.
    """
    def next_nodes(self,graph,current_id,signal):
        out=[]
        for e in graph.edges:
            if e.source!=current_id:continue
            if e.condition=="always":
                out.append(e.target)
            elif e.condition=="needs_tool" and signal.get("needs_tool"):
                out.append(e.target)
            elif e.condition=="medium_confidence" and .35<=signal.get("confidence",1)<.7:
                out.append(e.target)
            elif e.condition=="low_confidence_or_failure" and (
                signal.get("confidence",1)<.45 or not signal.get("success",True)
            ):
                out.append(e.target)
        return out
