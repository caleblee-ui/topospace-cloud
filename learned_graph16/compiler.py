
from execution_graph15.models import ExecutionNode,ExecutionEdge,ExecutionGraph

class LearnedPathCompiler:
    def compile(self,path_template):
        nodes=[];edges=[];prev=None
        for i,stage in enumerate(path_template.stages):
            kind="model" if stage in {"fast","balanced","reasoning"} else stage
            node=ExecutionNode(f"stage-{i}",kind,stage if kind=="model" else None,metadata={"stage":stage})
            nodes.append(node)
            if prev is not None:
                edges.append(ExecutionEdge(prev,node.id,"always",1.0))
            prev=node.id
        return ExecutionGraph(nodes,edges,nodes[0].id if nodes else None)
