
from unified_runtime.router import UnifiedAdaptiveRouter
from unified_runtime.planner import AdaptiveExecutionPlanner

class UnifiedAdaptiveAgentRuntime:
    def __init__(self):
        self.router=UnifiedAdaptiveRouter()
        self.planner=AdaptiveExecutionPlanner()
        self.history=[]

    def build_execution_space(self,agent_state,spaces):
        routes={}
        for domain in ("memory","tool","skill","plan"):
            routes[domain]=self.router.route(agent_state,domain,spaces.get(domain,[]))
        composed=self.planner.compose(routes)
        out={"task_id":agent_state.task_id,"routes":routes,**composed}
        self.history.append(out)
        return out

    def learn(self,execution_result,feedback_by_domain):
        rewards={}
        for domain,fb in feedback_by_domain.items():
            if domain not in execution_result["routes"]:
                continue
            rewards[domain]=self.router.feedback(
                execution_result["routes"][domain],
                relevant_selected=int(fb.get("relevant_selected",0)),
                total_relevant=int(fb.get("total_relevant",1)),
                violations=int(fb.get("violations",0)),
                latency_ms=float(fb.get("latency_ms",0)),
                token_cost=int(fb.get("token_cost",0))
            )
        return rewards
