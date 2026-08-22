
from __future__ import annotations
from typing import List, Dict
from runtime.hybrid_context import HybridTopologicalScorer
from multiagent.models import AgentNode, AgentTeam

class TopologicalTeamBuilder:
    """Selects and connects a task-specific agent team."""

    def __init__(self, scorer=None):
        self.scorer=scorer or HybridTopologicalScorer()

    def build(self, objective: str, agents: List[AgentNode], edges, max_agents=4, required_capabilities=None):
        nodes=[a.id for a in agents]
        dist={a.id:a.adaptive_distance for a in agents}
        pers={a.id:a.persistence for a in agents}
        drift={a.id:a.drift for a in agents}
        ranked=self.scorer.score(nodes,edges,dist,pers,drift)
        byid={a.id:a for a in agents}

        selected=[]
        covered=set()
        required=set(required_capabilities or [])
        for row in ranked:
            a=byid[row["id"]]
            selected.append({
                "id":a.id,
                "score":row["score"],
                "capabilities":list(a.capabilities),
                "risk":a.risk,
                "cost":a.cost,
                "reliability":a.reliability
            })
            covered.update(a.capabilities)
            if len(selected)>=max_agents and required.issubset(covered):
                break

        chosen={x["id"] for x in selected}
        team_edges=[e for e in edges if e[0] in chosen and e[1] in chosen]
        score=sum(x["score"] for x in selected)/max(1,len(selected))
        return AgentTeam(selected,team_edges,objective,score)
