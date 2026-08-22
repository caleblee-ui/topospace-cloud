
def geometry_reward(relevant_selected,total_relevant,selected_count,
                    violations=0,latency_ms=0.0,token_cost=0):
    precision=relevant_selected/max(1,selected_count)
    recall=relevant_selected/max(1,total_relevant)
    f1=0.0 if precision+recall==0 else 2*precision*recall/(precision+recall)
    penalty=2.0*violations + min(latency_ms/10000.0,.5) + min(token_cost/100000.0,.5)
    return f1-penalty
