
class PolicyTopologyBridge:
    """Maps learned/autopilot policy settings into topology runtime controls."""
    def apply(self,runtime,decision):
        eps=decision.get("epsilon")
        if eps is not None:
            runtime.rewirer.prune_threshold=max(.05,min(.4,float(eps)*.45))
        exploration=decision.get("exploration")
        if exploration is not None:
            runtime.rewirer.shortcut_threshold=max(.55,min(.95,.9-.3*float(exploration)))
        return {
          "prune_threshold":runtime.rewirer.prune_threshold,
          "shortcut_threshold":runtime.rewirer.shortcut_threshold
        }
