
# High-Performance Topology Core

v2.5 focuses on hot-path efficiency:
- incremental neighborhood membership updates
- topology delta propagation
- sharded object indexing
- dependency-free batch weighted-Lp distance
- persistent cache reference layer

The key architectural rule is to avoid whole-space recomputation when only a small fraction of
agent memory/tool/code objects change between steps.
