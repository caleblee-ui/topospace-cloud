
class CoupledFeedbackLearner:
    """Back-propagates domain rewards into coupling strengths."""
    def __init__(self,coupling,lr=.05):
        self.coupling=coupling;self.lr=lr

    def update(self,rewards):
        for src,row in self.coupling.matrix.items():
            sr=float(rewards.get(src,0))
            for dst,w in list(row.items()):
                dr=float(rewards.get(dst,0))
                # reinforce edges when source and target rewards agree positively
                signal=sr*dr
                row[dst]=max(-.5,min(.8,w+self.lr*signal))
        return self.coupling.matrix
