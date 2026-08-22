
def graph_topology_bucket(ctx):
    c=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity,ctx.coupling_strength)
    tools=min(1.0,ctx.expected_tool_calls/8)
    if c>=.75 or (c>=.6 and tools>.5):return "high"
    if c<=.30 and tools<=.25:return "low"
    return "medium"
