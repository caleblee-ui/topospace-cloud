
class StagedRolloutManager:
    STAGES=(5,25,50,100)
    def __init__(self):
        self.stage_index=-1
        self.active=False

    def start(self):
        self.stage_index=0;self.active=True
        return self.STAGES[self.stage_index]

    def advance(self):
        if not self.active:return None
        if self.stage_index>=len(self.STAGES)-1:
            self.active=False
            return 100
        self.stage_index+=1
        return self.STAGES[self.stage_index]

    def current(self):
        if self.stage_index<0:return 0
        return self.STAGES[self.stage_index]
