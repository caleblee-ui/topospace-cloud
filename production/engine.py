
from __future__ import annotations
import hashlib,json,time
from production.config import ProductionConfig
from production.cache import LRUCache
from production.guardrails import RuntimeGuardrails
from optimization.context_pruner import TopologicalContextPruner
from optimization.token_optimizer import TokenBudgetController,TokenBudget
from optimization.minimal_team import MinimalTeamOptimizer

class TopoSpaceEngine:
    """Production-facing optimization facade.

    It runs before an LLM call and returns the smallest admissible context/team
    under topology, token, and execution budgets. No model vendor dependency.
    """
    def __init__(self,config=None):
        self.config=config or ProductionConfig()
        self.pruner=TopologicalContextPruner()
        self.token=TokenBudgetController(TokenBudget(
            self.config.max_context_tokens,self.config.reserve_output_tokens))
        self.team=MinimalTeamOptimizer()
        self.guard=RuntimeGuardrails(self.config.max_agents,self.config.max_tool_calls,self.config.max_steps)
        self.cache=LRUCache(self.config.cache_size)
        self.metrics={"requests":0,"cache_hits":0,"fail_open":0,"latency_ms_total":0.0}

    def _key(self,objective,context,agents,required):
        raw=json.dumps([objective,context,agents,required],sort_keys=True,default=str).encode()
        return hashlib.sha256(raw).hexdigest()

    def optimize(self,objective,context,agents=None,required_capabilities=None):
        start=time.perf_counter();self.metrics["requests"]+=1
        agents=agents or []; required_capabilities=required_capabilities or []
        key=self._key(objective,context,agents,required_capabilities)
        hit=self.cache.get(key)
        if hit is not None:
            self.metrics["cache_hits"]+=1
            return dict(hit,cache_hit=True)
        try:
            p=self.pruner.prune(context,self.config.epsilon,self.config.min_relevance,self.config.max_drift)
            b=self.token.prune(p["kept"])
            team=self.team.optimize(agents,required_capabilities,min_marginal_utility=.20,max_agents=self.config.max_agents)
            result={
              "objective":objective,"context":b["kept"],"dropped_context":p["dropped"]+b["dropped"],
              "context_tokens":b["tokens"],"team":team,
              "guardrails":self.guard.validate(agents=len(team)),
              "cache_hit":False
            }
        except Exception as e:
            if not self.config.fail_open: raise
            self.metrics["fail_open"]+=1
            result={"objective":objective,"context":context,"dropped_context":[],"context_tokens":sum(int(x.get("tokens",0)) for x in context),
                    "team":agents[:self.config.max_agents],"guardrails":{"ok":False,"errors":["optimizer_fail_open"]},
                    "cache_hit":False,"error":str(e)}
        self.metrics["latency_ms_total"]+=(time.perf_counter()-start)*1000
        self.cache.put(key,result)
        return result

    def health(self):
        r=self.metrics["requests"]
        return {**self.metrics,"avg_latency_ms":self.metrics["latency_ms_total"]/max(1,r),
                "cache_hit_rate":self.metrics["cache_hits"]/max(1,r)}
