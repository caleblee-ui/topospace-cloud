
class GraphDecisionExplainer:
    def explain_step(self,step):
        return {
          "summary":f'{step["kind"]} node {step["to"]} was reached through {step["relation"]}.',
          "selection_value":round(step["value"],6),
          "from":step["from"],"to":step["to"],"relation":step["relation"],"kind":step["kind"]
        }
