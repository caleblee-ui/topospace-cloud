class ReleaseGuard:
 REQUIRED=("api_contract","full_regression","gateway_e2e","shadow_promotion","rollback","js_validation","sbom")
 def evaluate(self,c):
  m=[x for x in self.REQUIRED if not c.get(x)];return {"ga_ready":not m,"missing":m}
