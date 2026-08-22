
def topology_bucket(ctx):
    complexity=max(ctx.risk,ctx.ambiguity,ctx.topology_complexity,ctx.coupling_strength)
    tools=min(1.0,ctx.expected_tool_calls/8)
    if complexity>=.75:return "high"
    if complexity<=.30 and tools<=.25:return "low"
    return "medium"
