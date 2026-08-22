
from __future__ import annotations
from autopilot.models import RuntimeSignals,AutopilotDecision

class TopologyAutopilot:
    """Closed-loop controller for TopoSpace runtime parameters."""
    def __init__(self,
                 epsilon_bounds=(.16,.68),
                 p_bounds=(1.0,4.0),
                 token_bounds=(6000,48000),
                 memory_bounds=(4,30),
                 tool_radius_bounds=(.15,.70)):
        self.epsilon_bounds=epsilon_bounds
        self.p_bounds=p_bounds
        self.token_bounds=token_bounds
        self.memory_bounds=memory_bounds
        self.tool_radius_bounds=tool_radius_bounds

    @staticmethod
    def clip(x,b): return max(b[0],min(b[1],x))

    def decide(self,s:RuntimeSignals):
        reasons=[]
        need=.38*s.uncertainty+.24*s.drift+.18*(1-s.success_rate)+.10*s.tool_failure_rate+.10*(1-s.memory_hit_rate)
        pressure=.60*s.token_pressure+.40*s.latency_pressure

        if s.uncertainty>.7: reasons.append("expand_for_uncertainty")
        if s.drift>.45: reasons.append("expand_for_drift")
        if s.success_rate<.75: reasons.append("expand_for_quality")
        if pressure>.65: reasons.append("contract_for_cost_latency")
        if s.memory_hit_rate<.4: reasons.append("increase_memory_recall")
        if s.tool_failure_rate>.25: reasons.append("broaden_tool_neighborhood")
        if not reasons: reasons.append("stable_operating_point")

        eps=self.epsilon_bounds[0]+(self.epsilon_bounds[1]-self.epsilon_bounds[0])*need
        eps-=.16*pressure*(1-s.uncertainty)
        eps=self.clip(eps,self.epsilon_bounds)

        p=self.p_bounds[0]+(self.p_bounds[1]-self.p_bounds[0])*(.55*s.uncertainty+.45*s.drift)
        p=self.clip(p,self.p_bounds)

        budget_need=max(0,min(1,.62*need+.38*s.uncertainty-.25*pressure))
        tokens=round(self.token_bounds[0]+(self.token_bounds[1]-self.token_bounds[0])*budget_need)

        memory_need=max(0,min(1,.55*(1-s.memory_hit_rate)+.45*s.uncertainty))
        memory=round(self.memory_bounds[0]+(self.memory_bounds[1]-self.memory_bounds[0])*memory_need)

        tool_need=max(0,min(1,.55*s.tool_failure_rate+.45*s.uncertainty))
        tool_radius=self.tool_radius_bounds[0]+(self.tool_radius_bounds[1]-self.tool_radius_bounds[0])*tool_need

        exploration=max(0,min(1,.5*s.uncertainty+.3*s.drift+.2*(1-s.success_rate)))

        return AutopilotDecision(eps,p,tokens,memory,tool_radius,exploration,reasons)
