
class CrossDomainCoupling:
    """
    Coupling matrix C[a][b] means selections in domain a influence geometry in b.
    Positive values expand/reweight related neighborhoods; negative values contract them.
    """
    DEFAULT={
      "memory":{"tool":.28,"skill":.18,"plan":.32},
      "tool":{"memory":.12,"skill":.20,"plan":.36},
      "skill":{"memory":.10,"tool":.24,"plan":.25},
      "plan":{"memory":.18,"tool":.30,"skill":.16},
    }
    def __init__(self,matrix=None):
        self.matrix=matrix or self.DEFAULT

    def influence(self,source_domain,target_domain,selection_strength):
        return self.matrix.get(source_domain,{}).get(target_domain,0.0)*float(selection_strength)

    def total_for(self,target_domain,signals):
        # signals: {source_domain: strength}
        return sum(self.influence(src,target_domain,strength) for src,strength in signals.items())
