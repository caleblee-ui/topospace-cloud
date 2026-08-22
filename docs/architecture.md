
# Architecture

TopoSpace separates candidate generation, adaptive geometry, topological scoring, agent runtime,
and visualization.

`Agent -> Candidate Index -> Adaptive Geometry -> Hybrid Topological Context -> Runtime -> Graph Payload -> Web SDK`

The web component is independent of Python and consumes JSON payloads.
