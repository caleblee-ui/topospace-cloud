# TopoSpace 1.1 beta4 — Generalized Geometry Runtime

The runtime now follows the paper's admissible-aggregator abstraction. Lp is retained as one admissible geometry,
not the universal geometry. Supported reference aggregators include weighted Lp, weighted Chebyshev, nonnegative
conic combinations, maxima, concave reshaping, OWA and nested group geometries.

Every component view carries Metric/Pseudometric/Quasi-metric/Raw metadata. The runtime propagates this class into
an explicit guarantee set, so raw or directional views do not silently inherit planning, filtration or quotient
guarantees they do not mathematically support.

Nested geometry is intended for practical AI runtime policy: semantic evidence can be compensatory while
security/policy is bottleneck-like, then group distances can be combined at a higher level. A finite graph chain
distance provides the globally consistent planning-distance boundary for state-dependent local geometries.
