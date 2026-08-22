
# TopoSpace 1.1 Beta Runtime

beta1 packages the framework-agnostic lifecycle model as a deployable runtime server plus remote Python SDK.

Integration modes:
- embedded middleware for in-process custom agents,
- remote HTTP runtime for language/framework neutrality,
- optional framework adapters layered over the stable lifecycle contract.

The runtime server isolates middleware state per tenant. API key authentication, health/readiness endpoints,
Docker deployment assets and a stable adapter base are included. TorusDB remains the durable memory integration
boundary; production deployments should point the existing TorusDB HTTP adapter at the customer's service.
