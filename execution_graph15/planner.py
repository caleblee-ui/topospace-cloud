
from execution_graph15.models import ExecutionNode,ExecutionEdge,ExecutionGraph

class TopologyAwareExecutionGraphPlanner:
    """
    Builds a progressive execution graph instead of routing the full task to one model.
    """
    def build(self,ctx,model_route,has_tools=False,has_memory=False):
        nodes=[];edges=[]
        # Always begin with selected model class.
        primary=model_route["selected"]
        nodes.append(ExecutionNode("model-primary","model",primary,metadata={"role":"primary"}))
        entry="model-primary"

        if has_memory:
            nodes.insert(0,ExecutionNode("memory-recall","memory",metadata={"role":"context"}))
            edges.append(ExecutionEdge("memory-recall","model-primary","always",1.0))
            entry="memory-recall"

        if has_tools:
            nodes.append(ExecutionNode("tool-phase","tool",metadata={"role":"tool"}))
            edges.append(ExecutionEdge("model-primary","tool-phase","needs_tool",.9))

        complexity=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity,ctx.coupling_strength)
        if primary!="reasoning" and complexity>.55:
            nodes.append(ExecutionNode("model-reasoning","model","reasoning",metadata={"role":"escalation"}))
            src="tool-phase" if has_tools else "model-primary"
            edges.append(ExecutionEdge(src,"model-reasoning","low_confidence_or_failure",.85))

        if primary=="fast" and complexity>.30:
            nodes.append(ExecutionNode("model-balanced","model","balanced",metadata={"role":"escalation"}))
            edges.append(ExecutionEdge("model-primary","model-balanced","medium_confidence",.75))

        return ExecutionGraph(nodes,edges,entry)
