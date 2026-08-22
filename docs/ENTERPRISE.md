
# TopoSpace Enterprise Control Plane

v2.3 adds:
- RBAC and project scoping
- organization/project policy inheritance
- secret-provider abstraction
- tamper-evident hash-chained audit logs
- signed configuration bundles
- Prometheus-compatible metrics
- Redis distributed-state adapter interface
- PostgreSQL checkpoint adapter interface
- Kubernetes deployment and HPA manifests

The bundled Redis/PostgreSQL adapters are integration layers; the corresponding client libraries and managed services are deployment dependencies.
