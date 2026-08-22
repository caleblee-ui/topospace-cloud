
class TopologyAwareModelScorer:
    def __init__(self,history):
        self.history=history

    def score(self,profile,ctx):
        hist=self.history.stats(profile.name)
        complexity=max(ctx.ambiguity,ctx.topology_complexity,ctx.coupling_strength)
        reasoning_need=.45*complexity+.30*ctx.risk+.25*min(1,ctx.expected_tool_calls/8)
        latency_need=ctx.latency_pressure

        est_cost=(ctx.expected_input_tokens/1000)*profile.input_cost_per_1k + (ctx.expected_output_tokens/1000)*profile.output_cost_per_1k
        cost_eff=1/(1+est_cost)
        latency_eff=1/(1+profile.latency_ms/1000)

        return (
          .24*profile.quality +
          .20*(1-abs(profile.reasoning_affinity-reasoning_need)) +
          .10*profile.tool_affinity*min(1,ctx.expected_tool_calls/6) +
          .10*cost_eff +
          .10*latency_eff +
          .08*(1-abs(latency_need-(1-latency_eff))) +
          .10*hist["mean_reward"] +
          .08*hist["success_rate"]
        )
