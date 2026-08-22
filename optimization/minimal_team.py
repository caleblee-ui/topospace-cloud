
class MinimalTeamOptimizer:
    """Greedy minimal-capability cover with marginal-utility gating."""
    def optimize(self,members,required_capabilities=None,min_marginal_utility=.05,max_agents=8):
        required=set(required_capabilities or [])
        remaining=list(members); selected=[]; covered=set()
        while remaining and len(selected)<max_agents:
            def value(a):
                new=len(set(a.get("capabilities",[]))-covered)
                utility=float(a.get("score",0))*float(a.get("reliability",1))
                penalty=.35*float(a.get("cost",0))+.35*float(a.get("risk",0))
                return (new*2.0+utility-penalty,utility-penalty)
            best=max(remaining,key=value); total,marginal=value(best)
            newcaps=set(best.get("capabilities",[]))-covered
            if required.issubset(covered) and marginal<min_marginal_utility: break
            if not newcaps and required and not required.issubset(covered) and marginal<min_marginal_utility:
                remaining.remove(best);continue
            selected.append(best);covered.update(best.get("capabilities",[]));remaining.remove(best)
            if required.issubset(covered):
                # stop once required capabilities are covered unless a genuinely valuable collaborator remains
                extras=[value(a)[1] for a in remaining]
                if not extras or max(extras)<min_marginal_utility: break
        # enforce minimality: remove redundant members if coverage survives
        changed=True
        while changed:
            changed=False
            for a in list(selected):
                others=[x for x in selected if x is not a]
                cov=set().union(*(set(x.get("capabilities",[])) for x in others)) if others else set()
                if required.issubset(cov) and value(a)[1]<min_marginal_utility:
                    selected.remove(a);changed=True;break
        return selected
