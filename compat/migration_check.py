
class UpgradeMigrationCheck:
    def run(self,runner,target,context=None):
        before=runner.current_version
        applied=runner.migrate(target,context)
        after=runner.current_version
        return {"before":before,"after":after,"applied":applied,"ok":after==target}
