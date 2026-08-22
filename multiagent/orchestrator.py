
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Callable, List, Dict, Any
from multiagent.team_builder import TopologicalTeamBuilder
from multiagent.models import AgentNode
from topology.drift import TopologicalDrift
from learning.topology_learner import TopologyLearner
from learning.multi_objective import MultiObjectiveTopologyLearner

@dataclass
class MultiAgentStep:
    step:int
    team:list
    observation:dict
    team_drift:float
    reward:float
    rebuilt:bool

class AdaptiveMultiAgentRuntime:
    """Closed-loop multi-agent orchestration over a dynamic topology."""

    def __init__(self, max_steps=5, drift_threshold=.25):
        self.builder=TopologicalTeamBuilder()
        self.drift=TopologicalDrift()
        self.base_learner=TopologyLearner(seed=23)
        self.multi=MultiObjectiveTopologyLearner(self.base_learner)
        self.max_steps=max_steps
        self.drift_threshold=drift_threshold
        self.trace=[]

    @staticmethod
    def _snapshot(team):
        nodes=[x["id"] for x in team.members]
        edges=[(a,b) for a,b,*_ in team.topology_edges]
        return {"nodes":nodes,"edges":edges}

    def run(self, objective, agents:List[AgentNode], edges, executor:Callable[[dict,int],dict],
            required_capabilities=None, mutate=None):
        cur_agents=list(agents); cur_edges=list(edges)
        previous={"nodes":[],"edges":[]}

        for step in range(self.max_steps):
            team=self.builder.build(objective,cur_agents,cur_edges,max_agents=4,
                                    required_capabilities=required_capabilities)
            current=self._snapshot(team)
            report=self.drift.compare(previous,current)

            payload={
                "objective":objective,
                "team":team.members,
                "topology_edges":team.topology_edges,
                "topology":{
                    "p":self.base_learner.params.p,
                    "epsilon":self.base_learner.params.epsilon,
                    "weights":dict(self.base_learner.params.weights),
                }
            }
            obs=executor(payload,step)
            metrics={
                "success":1.0 if obs.get("success") else 0.0,
                "token_cost_norm":obs.get("token_cost_norm",0.0),
                "latency_norm":obs.get("latency_norm",0.0),
                "tool_calls_norm":obs.get("tool_calls_norm",0.0),
                "risk":obs.get("risk",0.0),
            }
            cand=self.base_learner.propose()
            _,reward=self.multi.update(cand,metrics)

            if mutate:
                cur_agents,cur_edges=mutate(cur_agents,cur_edges,obs,step,team)

            rebuilt=(not obs.get("success")) or report.score>=self.drift_threshold
            self.trace.append(MultiAgentStep(step,team.members,obs,report.score,reward,rebuilt))

            if obs.get("success"):
                break
            previous=current

        return {
            "success":bool(self.trace and self.trace[-1].observation.get("success")),
            "steps":[asdict(x) for x in self.trace],
            "final_topology":{
                "p":self.base_learner.params.p,
                "epsilon":self.base_learner.params.epsilon,
                "weights":dict(self.base_learner.params.weights),
            }
        }
